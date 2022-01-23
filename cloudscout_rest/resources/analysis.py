from flask import request
from flask_restful import Resource
from cloudscout_rest.ext import mongo
from cloudscout_rest.common.auth_required import auth_required
from cloudscout_rest.schema import FOOTBALL, get_stat_categories

def get_avg_aggregation(schema, category):
    agg = {'_id': '$meta.position'}
    categories = get_stat_categories(schema)
    for field in categories[category]:
        agg[field] = {'$avg': f'$stats.{category}.{field}'}
    return agg

class Analysis(Resource):
    @auth_required
    def get(self):
        players = mongo.db.players
        schema = FOOTBALL
        position = request.args.get('position')
        result = {}
        for category in get_stat_categories(schema):
            pipeline = []
            if position is not None:
                pipeline.append({
                    '$match': {
                        'meta.position': request.args.get('position')
                    }
                })

            # add { '$addFields': { 'position': '$_id' } } to include position
            # in response
            pipeline.extend([
                {
                    '$group': get_avg_aggregation(schema, category), 
                },
                {
                    '$project': {
                        '_id': False,
                    }
                },
            ])
            agg_result = list(players.aggregate(pipeline))
            if request.args.get('position'):
                # returns list with one arg
                result[category] = agg_result[0]
            else:
                result[category] = agg_result
        return result, 200
