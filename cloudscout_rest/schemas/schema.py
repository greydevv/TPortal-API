from cloudscout_rest.schemas.enums import Patterns, Sports
from cloudscout_rest.schemas.base import PlayerSchema, SchemaObject

def make_array(schema):
    return {
        'type': 'array',
        'items': schema.raw() if isinstance(schema, SchemaObject) else schema
    }

def get_stat_mapping(schema):
    stats = schema['properties']['stats']['properties']
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
            },
            'additionalProperties': False,
            'required': [
                'first',
                'last',
                'institution',
            ]
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
                    'required': [
                        'divisions',
                        'classes',
                        'positions'
                    ]
                }
            },
            'additionalProperties': False,
            'required': [
                'favorites',
                'default_filters'
            ]
        },
    },
    'additionalProperties': False,
    'required': [
        'uid',
        'meta',
        'account',
    ]
}


# FOOTBALL = make_schema(Positions.FOOTBALL.value, Positions.FOOTBALL.name, {
#     'type': 'object',
#     'properties': {
#         'general': {
#             'type': 'object',
#             'properties': {
#                 'all_purpose_plays': {'type': ['number', 'null']},
#                 'all_purpose_yds': {'type': ['number', 'null']},
#                 'all_purpose_yds_per_game': {'type': ['number', 'null']},
#                 'games_played': {'type': ['number', 'null']},
#                 'games_started': {'type': ['number', 'null']},
#                 'points': {'type': ['number', 'null']},
#                 'touchdowns': {'type': ['number', 'null']},
#             },
#             'additionalProperties': False,
#         },
#         'offensive': {
#             'type': 'object',
#             'properties': {
#                 'completion_pct': {'type': ['number', 'null']},
#                 'completions_per_game': {'type': ['number', 'null']},
#                 'first_downs': {'type': ['number', 'null']},
#                 'first_downs_passing': {'type': ['number', 'null']},
#                 'first_downs_rushing': {'type': ['number', 'null']},
#                 'fumbles_lost': {'type': ['number', 'null']},
#                 'interceptions': {'type': ['number', 'null']},
#                 'pass_attempts': {'type': ['number', 'null']},
#                 'passing_eff': {'type': ['number', 'null']},
#                 'passing_tds': {'type': ['number', 'null']},
#                 'passing_yds': {'type': ['number', 'null']},
#                 'passing_yds_per_game': {'type': ['number', 'null']},
#                 'penalties': {'type': ['number', 'null']},
#                 'penalties_per_game': {'type': ['number', 'null']},
#                 'penalty_yds': {'type': ['number', 'null']},
#                 'penalty_yds_per_game': {'type': ['number', 'null']},
#                 'plays': {'type': ['number', 'null']},
#                 'receiving_longest': {'type': ['number', 'null']},
#                 'receiving_tds': {'type': ['number', 'null']},
#                 'receiving_yds': {'type': ['number', 'null']},
#                 'receiving_yds_per_game': {'type': ['number', 'null']},
#                 'receptions': {'type': ['number', 'null']},
#                 'receptions_per_game': {'type': ['number', 'null']},
#                 'redzone_attempts': {'type': ['number', 'null']},
#                 'redzone_passing_tds': {'type': ['number', 'null']},
#                 'redzone_pts': {'type': ['number', 'null']},
#                 'redzone_rushing_tds': {'type': ['number', 'null']},
#                 'redzone_scores': {'type': ['number', 'null']},
#                 'rush_attempts': {'type': ['number', 'null']},
#                 'rush_net_yds': {'type': ['number', 'null']},
#                 'rush_yds_per_game': {'type': ['number', 'null']},
#                 'rushing_longest': {'type': ['number', 'null']},
#                 'rushing_tds': {'type': ['number', 'null']},
#                 'rushing_yds': {'type': ['number', 'null']},
#                 'rushing_yds_lost': {'type': ['number', 'null']},
#                 'third_att': {'type': ['number', 'null']},
#                 'third_conv': {'type': ['number', 'null']},
#                 'total_offensive_plays': {'type': ['number', 'null']},
#                 'total_offensive_yds': {'type': ['number', 'null']},
#                 'total_offensive_yds_per_game': {'type': ['number', 'null']},
#                 'total_offensive_yds_per_play': {'type': ['number', 'null']},
#                 'yds': {'type': ['number', 'null']},
#                 'yds_per_completion': {'type': ['number', 'null']},
#                 'yds_per_play': {'type': ['number', 'null']},
#                 'yds_per_reception': {'type': ['number', 'null']},
#                 'yds_per_rush': {'type': ['number', 'null']},
#             },
#             'additionalProperties': False,
#         },
#         'defensive': {
#             'type': 'object',
#             'properties': {
#                 'blocked': {'type': ['number', 'null']},
#                 'fumbles_forced': {'type': ['number', 'null']},
#                 'fumbles_recovered': {'type': ['number', 'null']},
#                 'fumbles_returned': {'type': ['number', 'null']},
#                 'fumbles_returned_tds': {'type': ['number', 'null']},
#                 'interception_yds': {'type': ['number', 'null']},
#                 'interceptions': {'type': ['number', 'null']},
#                 'interceptions_returned_tds': {'type': ['number', 'null']},
#                 'pass_breakups': {'type': ['number', 'null']},
#                 'passes_defended': {'type': ['number', 'null']},
#                 'pts_off_turnover': {'type': ['number', 'null']},
#                 'redzone_end_downs': {'type': ['number', 'null']},
#                 'redzone_end_interceptions': {'type': ['number', 'null']},
#                 'sack_yds': {'type': ['number', 'null']},
#                 'sacks_assisted': {'type': ['number', 'null']},
#                 'sacks_solo': {'type': ['number', 'null']},
#                 'sacks_unassisted': {'type': ['number', 'null']},
#                 'safeties': {'type': ['number', 'null']},
#                 'tackle_yds': {'type': ['number', 'null']},
#                 'tackles': {'type': ['number', 'null']},
#                 'tackles_assisted': {'type': ['number', 'null']},
#                 'tackles_for_loss_assisted': {'type': ['number', 'null']},
#                 'tackles_for_loss_solo': {'type': ['number', 'null']},
#                 'tackles_solo': {'type': ['number', 'null']},
#             },
#             'additionalProperties': False,
#         },
#         'special': {
#             'type': 'object',
#             'properties': {
#                 'fc_yds': {'type': ['number', 'null']},
#                 'fga1_19': {'type': ['number', 'null']},
#                 'fga20_29': {'type': ['number', 'null']},
#                 'fga30_39': {'type': ['number', 'null']},
#                 'fga40_49': {'type': ['number', 'null']},
#                 'fga50_59': {'type': ['number', 'null']},
#                 'fga60': {'type': ['number', 'null']},
#                 'fgm1_19': {'type': ['number', 'null']},
#                 'fgm20_29': {'type': ['number', 'null']},
#                 'fgm30_39': {'type': ['number', 'null']},
#                 'fgm40_49': {'type': ['number', 'null']},
#                 'fgm50_59': {'type': ['number', 'null']},
#                 'fgm60': {'type': ['number', 'null']},
#                 'field_goal_blocks_allowed': {'type': ['number', 'null']},
#                 'field_goals': {'type': ['number', 'null']},
#                 'field_goals_attempted': {'type': ['number', 'null']},
#                 'field_goals_made': {'type': ['number', 'null']},
#                 'fumble_return_pat': {'type': ['number', 'null']},
#                 'kick_pat': {'type': ['number', 'null']},
#                 'kick_return_pat': {'type': ['number', 'null']},
#                 'kickoff_return_tds': {'type': ['number', 'null']},
#                 'kickoff_return_yds': {'type': ['number', 'null']},
#                 'kickoff_returns': {'type': ['number', 'null']},
#                 'kickoff_touchbacks': {'type': ['number', 'null']},
#                 'kickoff_yds': {'type': ['number', 'null']},
#                 'kickoffs': {'type': ['number', 'null']},
#                 'longest_fgm': {'type': ['number', 'null']},
#                 'net_kickoff_yds': {'type': ['number', 'null']},
#                 'net_punt_yds': {'type': ['number', 'null']},
#                 'onside_attempts': {'type': ['number', 'null']},
#                 'pass_2pt_att': {'type': ['number', 'null']},
#                 'pass_2pt_conv': {'type': ['number', 'null']},
#                 'pat_att': {'type': ['number', 'null']},
#                 'punt_longest': {'type': ['number', 'null']},
#                 'punt_return_tds': {'type': ['number', 'null']},
#                 'punt_return_yds': {'type': ['number', 'null']},
#                 'punt_returns': {'type': ['number', 'null']},
#                 'punt_touchbacks': {'type': ['number', 'null']},
#                 'punt_yds': {'type': ['number', 'null']},
#                 'punts': {'type': ['number', 'null']},
#                 'punts_inside_twenty': {'type': ['number', 'null']},
#                 'receiving_pat': {'type': ['number', 'null']},
#                 'redzone_end_field_goal': {'type': ['number', 'null']},
#                 'redzone_end_fumble': {'type': ['number', 'null']},
#                 'redzone_fg_made': {'type': ['number', 'null']},
#                 'rush_2pt_att': {'type': ['number', 'null']},
#                 'rush_pat': {'type': ['number', 'null']},
#                 'successful_onside_kicks': {'type': ['number', 'null']},
#             },
#             'additionalProperties': False,
#         },
#     },
#     'additionalProperties': False,
#     'required': [
#         'general',
#         'offensive',
#         'defensive',
#         'special',
#     ]
# })

# BASEBALL = make_schema(Positions.BASEBALL.value, Positions.BASEBALL.name, {
#     'additionalProperties': False,
#     'required': [

#     ]
# })
