from cloudscout_rest.schemas.enums import Patterns, Sports
from cloudscout_rest.schemas.base import PlayerSchema, SchemaObject

def make_array(schema):
    return {
        'type': 'array',
        'items': schema.raw() if isinstance(schema, SchemaObject) else schema
    }

def get_stat_mapping(schema):
    stats = schema.raw()['properties']['stats']['properties']
    stat_map = {}
    for category in stats.keys():
        stat_map[category] = list(stats[category]['properties'].keys())
    return stat_map

IDS = {
    'type': 'array',
    'items': {
        'type': 'string', 
        'pattern': Patterns.ID.value,
    }
}

USER = {
    'type': 'object',
    'properties': {
        'uid': {'type': 'string', 'pattern': Patterns.USER_ID.value},
        'meta': {
            'type': 'object',
            'properties': {
                'first': {'type': 'string'},
                'last': {'type': 'string'},
                'institution': {'type': 'string'},
                'sport': {'type': 'string', 'enum': Sports.get_names()}
            },
            'additionalProperties': False,
            'required': ['first', 'last', 'institution']
        },
        'account': {
            'type': 'object',
            'properties': {
                'favorites': IDS,
                'sport': {'type': 'string'},
                'default_filters': {
                    'type': 'object',
                    'properties': {
                        'divisions': {
                            'type': 'array',
                            'items': {
                                'type': ['number', 'null'],
                                'enum': [None,1,2,3]
                            }
                        },
                        'classes': {
                            'type': 'array',
                            'items': {
                                'type': ['number', 'null'],
                                'enum': [None,1,2,3,4,5]
                            }
                        },
                        'positions': {
                            'type': 'array',
                            'items': {
                                'type': ['string', 'null'],
                            }
                        }
                    },
                    'additionalProperties': False,
                    'required': ['divisions', 'classes', 'positions']
                },
                'advanced_filters': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'stat': {'type': 'string'},
                            'op': {'type': 'string', 'enum': ['gt', 'lt', 'eq']},
                            'value': {'type': 'number'}
                        },
                        'additionalProperties': False,
                        'required': ['stat', 'op', 'value']
                    }
                }
            },
            'additionalProperties': False,
            'required': ['favorites', 'default_filters', 'advanced_filters']
        },
    },
    'additionalProperties': False,
    'required': ['uid', 'meta', 'account']
}
