from flask import request, make_response
from flask_restful import Resource
import jsonschema
from tportal_rest.ext import mongo
from tportal_rest.exceptions import PlayerNotFoundError, DuplicateKeyError
from tportal_rest.schema import FOOTBALL_SCHEMA

def is_valid_json(json):
    try:
        jsonschema.validate(instance=json, schema=FOOTBALL_SCHEMA)
        return True
    except jsonschema.ValidationError:
        return False

class Players(Resource):
    def get(self):
        players = mongo.db.players
        pipeline = self.__build_pipeline(request.args)
        data = list(players.aggregate(pipeline))
        return data, 200
    
    def put(self):
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

    def post(self):
        if not is_valid_json(request.json):
            return {'message': 'invalid JSON'}, 400
        players = mongo.db.players
        dup_pids = self.__get_dup_pids(request.json)
        if dup_pids:
            raise DuplicateKeyError(data=dup_pids)
        ins_result = players.insert_many(request.json)
        return [e['pid'] for e in request.json], 200

    def delete(self):
        if not request.json:
            return '', 204
        players = mongo.db.players
        pids = list(filter(lambda x: isinstance(x, str), request.json))
        result = players.delete_many({'pid': {'$in':pids}})
        return '', 204

    @staticmethod
    def __build_pipeline(args):
        pipeline = []
        if args.get('q'):
            query = args.get('q')
            pipeline.append({'$search': {'text': {'query': query, 'path': {'wildcard': '*'}}}})
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
    def get(self, pid):
        players = mongo.db.players
        data = players.find_one({'pid': pid}, {'_id': False})
        if not data:
            raise PlayerNotFoundError(data=pid)
        return data, 200

    def delete(self, pid):
        players = mongo.db.players
        result = players.delete_one({'pid': pid})
        if result.deleted_count == 0:
            raise PlayerNotFoundError(data=pid)
        return '', 204
