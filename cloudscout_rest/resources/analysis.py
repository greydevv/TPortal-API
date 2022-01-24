from flask import request
from flask_restful import Resource
from cloudscout_rest.ext import mongo
from cloudscout_rest.common.auth_required import auth_required
from cloudscout_rest.schema import FOOTBALL, get_stat_mapping

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
    # @auth_required
    def get(self):
        players = mongo.db.players
        schema = FOOTBALL
        pipeline = []
        position = request.args.get('position')
        if position is not None:
            pipeline.append({
                '$match': {'meta.position': position}
            })
        pipeline.extend(build_group_aggregation(schema))
        if position is not None:
            # list is returned from aggregate with always one element, just
            # return that instead
            return list(players.aggregate(pipeline))[0], 200
        return list(players.aggregate(pipeline)), 200
