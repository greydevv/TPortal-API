from flask import request
from flask_restful import Resource
# from flask_jwt_extended import jwt_required
from cloudscout_rest.ext import mongo
from cloudscout_rest.exceptions import DuplicateKeyError, ResourceNotFoundError
from cloudscout_rest.schema import make_array, FOOTBALL, IDS
from cloudscout_rest.common.validate_json import assertjson
from cloudscout_rest.common.auth_required import auth_required

class Players(Resource):
    @auth_required
    def get(self):
        players = mongo.db.players
        pipeline = self.__build_pipeline(request.args)
        data = list(players.aggregate(pipeline))
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
        if args.get('positions'):
            pipeline.append({'$match': {'meta.position': {'$in': [arg.upper() for arg in args['position'].split(',')]}}})
        if args.get('divisions'):
            pipeline.append({'$match': {'meta.division': {'$in': [int(arg) for arg in args['division'].split(',')]}}})
        if args.get('classes'):
            pipeline.append({'$match': {'meta.class': {'$in': [int(arg) for arg in args['class'].split(',')]}}})
        if args.get('limit') and args.get('limit').isnumeric():
            pipeline.append({'$limit': int(args['limit'])})
        if args.get('pids'):
            pipeline.append({'$match': {'pid': {'$in': [arg for arg in args['pids'].split(',')]}}})
        pipeline.append({'$project': {'_id': False}})
        if not args.get('q'):
            pipeline.append({'$sort': {'meta.date': -1}})
        else:
            pipeline.append({
                '$sort': {
                    'meta.institution': {'$meta': 'textScore'},
                    'meta.last': {'$meta': 'textScore'},
                    'meta.first': {'$meta': 'textScore'},
                    # SHOULDN'T I BE SORTING BY DATE?
                    '_id': 1,
                }})
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
