from flask import request
from flask_restful import Resource
from cloudscout_rest.ext import mongo
from cloudscout_rest.common.auth_required import auth_required
from cloudscout_rest.schema import FOOTBALL

def get_avg_aggregation(category, fields):
    agg = {'_id': None}
    for field in fields:
        agg[field] = {'$avg': f'$stats.{category}.{field}'}
    return agg

def get_stat_fields(schema):
    return schema['properties']['stats']['required']

def get_category_stats(category, schema):
    return list(schema['properties']['stats']['properties'][category]['properties'].keys())

class Analysis(Resource):
    @auth_required
    def get(self):
        players = mongo.db.players
        result = {}
        schema = FOOTBALL
        for category in get_stat_fields(schema):
            agg_result = players.aggregate([
                {
                    '$group': get_avg_aggregation(
                        category, 
                        get_category_stats(category, schema)
                    )
                }
            ])
            result[category] = list(agg_result)
        return result, 200
