from flask import request, jsonify
from flask_restful import Resource
from cloudscout_rest.ext import mongo
from cloudscout_rest.exceptions import DuplicateKeyError, ResourceNotFoundError
from cloudscout_rest.schemas.schema import make_array, IDS
from cloudscout_rest.schemas.players import FOOTBALL
from cloudscout_rest.common.validate_json import assertjson
from cloudscout_rest.common.auth_required import auth_required

class Players(Resource):
    # @auth_required
    def get(self):
        players = mongo.db.players
        pipeline = self.__build_pipeline(request.args)
        data = list(players.aggregate(pipeline))[0]
        return data, 200
    
    @auth_required
    @assertjson(make_array(FOOTBALL))
    def put(self):
        players = mongo.db.players
        pids = [e['pid'] for e in request.json]
        for pid in pids:
            if not players.find_one({'pid': pid}, {'_id': False}):
                raise ResourceNotFoundError(data=pid)
        players.delete_many({'pid': {'$in':pids}})
        ins_result = players.insert_many(request.json)
        return {}, 200

    @auth_required
    @assertjson(make_array(FOOTBALL))
    def post(self):
        players = mongo.db.players
        dup_pids = self.__get_dup_pids(request.json)
        if dup_pids:
            raise DuplicateKeyError(data=dup_pids)
        ins_result = players.insert_many(request.json)
        return {}, 200

    @auth_required
    @assertjson(IDS)
    def delete(self):
        players = mongo.db.players
        result = players.delete_many({'pid': {'$in': request.json}})
        return {}, 200

    @staticmethod
    def __build_pipeline(args):
        pipeline = []
        if args.get('q'):
            query = args.get('q')
            pipeline.append({'$search': {'text': {'query': query, 'fuzzy': {}, 'path': ['meta.first', 'meta.last', 'meta.institution']}}})
            pipeline.append({
                '$sort': {
                    'meta.institution': {'$meta': 'textScore'},
                    'meta.last': {'$meta': 'textScore'},
                    'meta.first': {'$meta': 'textScore'},
                    # SHOULDN'T I BE SORTING BY DATE?
                    '_id': 1,
            }})
        else:
            pipeline.append({'$sort': {'meta.date': -1, '_id': -1}})
        if args.get('positions'):
            pipeline.append({'$match': {'meta.position': {'$in': [arg.upper() for arg in args['positions'].split(',')]}}})
        if args.get('divisions'):
            pipeline.append({'$match': {'meta.division': {'$in': [int(arg) for arg in args['divisions'].split(',')]}}})
        if args.get('advanced'):
            for f in args['advanced'].split(','):
                f_split = f.split(';')
                stat = f'stats.{f_split[0]}'
                op = f'${f_split[1]}'
                value = float(f_split[2])
                pipeline.append({'$match': {stat: {op: value}}})
        if args.get('classes'):
            pipeline.append({'$match': {'meta.class': {'$in': [int(arg) for arg in args['classes'].split(',')]}}})
        if args.get('pids'):
            pipeline.append({'$match': {'pid': {'$in': [arg for arg in args['pids'].split(',')]}}})

        limit = 50
        if args.get('limit') and args.get('limit').isnumeric():
            limit = int(args['limit'])
            # pipeline.append({'$limit': int(args['limit'])})
        page = 1
        if args.get('page') and args.get('page').isnumeric():
            page = int(args['page'])
        pipeline.append({
            '$facet': {
                'total': [{'$count': 'total'}],
                'data': [{'$skip': (page-1)*limit}, {'$limit': limit}, {'$project': {'_id': False}}] 
            }
        })
        pipeline.append({'$addFields': {'total': {'$ifNull': [{'$arrayElemAt': ['$total.total', 0]}, 0]}}})
        return pipeline

    @staticmethod
    def __get_dup_pids(json):
        players = mongo.db.players
        dup_pids = []
        if isinstance(json, list):
            pids = [e['pid'] for e in json]
            dup_pids = [dup['pid'] for dup in players.find({'pid': {'$in':pids}})]
        else:
            if players.find_one({'pid':json['pid']}):
                dup_pids = [json['pid']]
        return dup_pids

class Player(Resource):
    @auth_required
    def get(self, pid):
        players = mongo.db.players
        data = players.find_one({'pid': pid}, {'_id': False})
        if not data:
            raise ResourceNotFoundError(data=pid)
        return data, 200

    @auth_required
    def delete(self, pid):
        players = mongo.db.players
        result = players.delete_one({'pid': pid})
        if result.deleted_count == 0:
            raise PlayerNotFoundError(data=pid)
        return {}, 200
