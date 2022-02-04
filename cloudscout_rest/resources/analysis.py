from flask import request
from flask_restful import Resource
from cloudscout_rest.ext import mongo
from cloudscout_rest.schemas.schema import get_stat_mapping
from cloudscout_rest.common.auth_required import auth_required
from cloudscout_rest.schemas.players import SPORT_NAME_MAPPING

def build_group_aggregation(schema):
    stat_mapping = get_stat_mapping(schema)
    grouping = {'_id': '$meta.position'}
    projection = {'_id': False, 'position': '$_id'}
    for category,stats in stat_mapping.items():
        sub_proj = {}
        for stat in stats:
            group_stat = f'{category}-{stat}'
            grouping[group_stat] = {'$avg': f'$stats.{category}.{stat}'}
            sub_proj[stat] = f'${group_stat}'
        projection[category] = sub_proj

    return [
        {'$group': grouping},
        {'$project': projection}
    ]

class Analysis(Resource):
    @auth_required
    def get(self):
        if request.args.get('sport') is None:
            return {'msg': "expected required 'sport' argument"}, 400
        if request.args.get('position') is None:
            return {'msg': "expected required 'position' argument"}, 400

        players = mongo.db.players
        schema = SPORT_NAME_MAPPING.get(request.args['sport'])
        position = request.args['position']
        pipeline = [{'$match': {'meta.position': position}}]
        pipeline.extend(build_group_aggregation(schema))
        data = list(players.aggregate(pipeline))[0]
        return data, 200
