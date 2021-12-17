from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from cloudscout_rest.ext import mongo
from cloudscout_rest.exceptions import DuplicateKeyError, PlayerNotFoundError
from cloudscout_rest.schema import FOOTBALL, IDS
from cloudscout_rest.common.validate_json import assertjson

class Players(Resource):
    @jwt_required()
    def get(self):
        players = mongo.db.players
        pipeline = self.__build_pipeline(request.args)
        data = list(players.aggregate(pipeline))
        return data, 200
    
    @jwt_required()
    @assertjson(FOOTBALL)
    def put(self):
        players = mongo.db.players
        if not request.json:
            return '', 204
        players = mongo.db.players
        pids = [e['pid'] for e in request.json]
        for pid in pids:
            if not players.find_one({'pid': pid}, {'_id': False}):
                raise PlayerNotFoundError(data=pid)
        players.delete_many({'pid': {'$in':pids}})
        ins_result = players.insert_many(request.json)
        return '', 204

    @jwt_required()
    @assertjson(FOOTBALL)
    def post(self):
        players = mongo.db.players
        dup_pids = self.__get_dup_pids(request.json)
        if dup_pids:
            raise DuplicateKeyError(data=dup_pids)
        ins_result = players.insert_many(request.json)
        return [e['pid'] for e in request.json], 200

    @jwt_required()
    @assertjson(IDS)
    def delete(self):
        players = mongo.db.players
        result = players.delete_many({'pid': {'$in': request.json}})
        return '', 204

    @staticmethod
    def __build_pipeline(args):
        pipeline = []
        if args.get('q'):
            query = args.get('q')
            pipeline.append({'$search': {'text': {'query': query, 'fuzzy': {}, 'path': ['meta.first', 'meta.last', 'meta.institution']}}})
        if args.get('position'):
            pos = args['position']
            pipeline.append({'$match': {'meta.position': {'$regex': f'^{pos}$', '$options': 'i'}}})
        if args.get('division'):
            pipeline.append({'$match': {'meta.division': int(args['division'])}})
        if args.get('year'):
            pipeline.append({'$match': {'meta.year': int(args['year'])}})
        if args.get('limit') and args.get('limit').isnumeric():
            pipeline.append({'$limit': int(args['limit'])})
        pipeline.append({'$project': {'_id': False}})
        if not args.get('q'):
            pipeline.append({'$sort': {'meta.date': 1}})
        else:
            pipeline.append({
                '$sort': {
                    'meta.institution': {'$meta': 'textScore'},
                    'meta.last': {'$meta': 'textScore'},
                    'meta.first': {'$meta': 'textScore'},
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
    @jwt_required()
    def get(self, pid):
        players = mongo.db.players
        data = players.find_one({'pid': pid}, {'_id': False})
        if not data:
            raise PlayerNotFoundError(data=pid)
        return data, 200

    @jwt_required()
    def delete(self, pid):
        players = mongo.db.players
        result = players.delete_one({'pid': pid})
        if result.deleted_count == 0:
            raise PlayerNotFoundError(data=pid)
        return '', 204
