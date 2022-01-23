class Patterns:
    USER_ID = r'^[0-9a-z]+$'
    ID = r'^[0-9]{10}$'
    EMAIL = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    YEAR_RANGE = r'^[0-9]{2}-[0-9]{2}$'

class Sports:
    FOOTBALL = 'FOOTBALL'
    BASEBALL = 'BASEBALL'
    MENS_BBALL = 'MENS_BASKETBALL'
    WOMENS_BBALL = 'WOMENS_BASKETBALL'

class Positions:
    FOOTBALL = [None, 'QB', 'WR', 'OL', 'RB', 'TE', 'C', 'OT', 'FB', 'DL', 'DT', 'DE', 'LB', 'DB', 'CB', 'S', 'P', 'K', 'LS']

def make_array(schema):
    return {
        'type': 'array',
        'items': schema
    }

def get_stat_categories(schema):
    stats = schema['properties']['stats']
    categories = stats['required']
    fields = {}
    for category in categories:
        fields[category] = list(stats['properties'][category]['properties'].keys())
    return fields

IDS = {
    'type': 'array',
    'items': {
        'type': 'string', 
        'pattern': Patterns.ID,
    }
}

USER = {
    'type': 'object',
    'properties': {
        'uid': {'type': 'string', 'pattern': Patterns.USER_ID},
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
                'default_filters': {
                    'type': 'object',
                    'properties': {
                        'division': {
                            'type': 'array',
                            'items': {
                                'type': ['number', 'null'],
                                'enum': [None,1,2,3]
                            }
                        },
                        'class': {
                            'type': 'array',
                            'items': {
                                'type': ['number', 'null'],
                                'enum': [None,1,2,3,4,5]
                            }
                        },
                        'position': {
                            'type': 'array',
                            'items': {
                                'type': ['string', 'null'],
                                'enum': Positions.FOOTBALL
                            }
                        }
                    },
                    'additionalProperties': False,
                    'required': [
                        'division',
                        'class',
                        'position'
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
FOOTBALL = {
    'type' : 'object',
    'properties' : {
        'pid': {'type': 'string', 'pattern': Patterns.ID},
        'meta': {
            'type': 'object',
            'properties': {
                'class': {'type': ['number', 'null'], 'enum': [None,1,2,3,4,5]},
                'conference': {'type': ['string', 'null']},
                'date': {'type': ['number', 'null']}, # Unix time epoch (seconds since Jan 1, 1970)
                'division': {'type': ['number', 'null'], 'enum': [None,1,2,3]},
                'first': {'type': ['string', 'null']},
                'institution': {'type': ['string', 'null']},
                'last': {'type': ['string', 'null']},
                'position': {'type': ['string', 'null'], 'enum': Positions.FOOTBALL},
                # include gender?
                'sport': {'type': ['string', 'null'], 'const': Sports.FOOTBALL},
                'year': {'type': ['string', 'null'], 'pattern': Patterns.YEAR_RANGE},
            },
            'additionalProperties': False,
            'required': [
                'class',
                'conference',
                'date',
                'division',
                'first',
                'last',
                'position',
                'sport',
                'year',
            ],
        },
        'stats': {
            'type': 'object',
            'properties': {
                'general': {
                    'type': 'object',
                    'properties': {
                        'all_purpose_plays': {'type': ['number', 'null']},
                        'all_purpose_yds': {'type': ['number', 'null']},
                        'all_purpose_yds_per_game': {'type': ['number', 'null']},
                        'games_played': {'type': ['number', 'null']},
                        'games_started': {'type': ['number', 'null']},
                        'points': {'type': ['number', 'null']},
                        'touchdowns': {'type': ['number', 'null']},
                    },
                    'additionalProperties': False,
                },
                'offensive': {
                    'type': 'object',
                    'properties': {
                        'completion_pct': {'type': ['number', 'null']},
                        'completions_per_game': {'type': ['number', 'null']},
                        'first_downs': {'type': ['number', 'null']},
                        'first_downs_passing': {'type': ['number', 'null']},
                        'first_downs_rushing': {'type': ['number', 'null']},
                        'fumbles_lost': {'type': ['number', 'null']},
                        'interceptions': {'type': ['number', 'null']},
                        'pass_attempts': {'type': ['number', 'null']},
                        'passing_eff': {'type': ['number', 'null']},
                        'passing_tds': {'type': ['number', 'null']},
                        'passing_yds': {'type': ['number', 'null']},
                        'passing_yds_per_game': {'type': ['number', 'null']},
                        'penalties': {'type': ['number', 'null']},
                        'penalties_per_game': {'type': ['number', 'null']},
                        'penalty_yds': {'type': ['number', 'null']},
                        'penalty_yds_per_game': {'type': ['number', 'null']},
                        'plays': {'type': ['number', 'null']},
                        'receiving_longest': {'type': ['number', 'null']},
                        'receiving_tds': {'type': ['number', 'null']},
                        'receiving_yds': {'type': ['number', 'null']},
                        'receiving_yds_per_game': {'type': ['number', 'null']},
                        'receptions': {'type': ['number', 'null']},
                        'receptions_per_game': {'type': ['number', 'null']},
                        'redzone_attempts': {'type': ['number', 'null']},
                        'redzone_passing_tds': {'type': ['number', 'null']},
                        'redzone_pts': {'type': ['number', 'null']},
                        'redzone_rushing_tds': {'type': ['number', 'null']},
                        'redzone_scores': {'type': ['number', 'null']},
                        'rush_attempts': {'type': ['number', 'null']},
                        'rush_net_yds': {'type': ['number', 'null']},
                        'rush_yds_per_game': {'type': ['number', 'null']},
                        'rushing_longest': {'type': ['number', 'null']},
                        'rushing_tds': {'type': ['number', 'null']},
                        'rushing_yds': {'type': ['number', 'null']},
                        'rushing_yds_lost': {'type': ['number', 'null']},
                        'third_att': {'type': ['number', 'null']},
                        'third_conv': {'type': ['number', 'null']},
                        'total_offensive_plays': {'type': ['number', 'null']},
                        'total_offensive_yds': {'type': ['number', 'null']},
                        'total_offensive_yds_per_game': {'type': ['number', 'null']},
                        'total_offensive_yds_per_play': {'type': ['number', 'null']},
                        'yds': {'type': ['number', 'null']},
                        'yds_per_completion': {'type': ['number', 'null']},
                        'yds_per_play': {'type': ['number', 'null']},
                        'yds_per_reception': {'type': ['number', 'null']},
                        'yds_per_rush': {'type': ['number', 'null']},
                    },
                    'additionalProperties': False,
                },
                'defensive': {
                    'type': 'object',
                    'properties': {
                        'blocked': {'type': ['number', 'null']},
                        'fumbles_forced': {'type': ['number', 'null']},
                        'fumbles_recovered': {'type': ['number', 'null']},
                        'fumbles_returned': {'type': ['number', 'null']},
                        'fumbles_returned_tds': {'type': ['number', 'null']},
                        'interception_yds': {'type': ['number', 'null']},
                        'interceptions': {'type': ['number', 'null']},
                        'interceptions_returned_tds': {'type': ['number', 'null']},
                        'pass_breakups': {'type': ['number', 'null']},
                        'passes_defended': {'type': ['number', 'null']},
                        'pts_off_turnover': {'type': ['number', 'null']},
                        'redzone_end_downs': {'type': ['number', 'null']},
                        'redzone_end_interceptions': {'type': ['number', 'null']},
                        'sack_yds': {'type': ['number', 'null']},
                        'sacks_assisted': {'type': ['number', 'null']},
                        'sacks_solo': {'type': ['number', 'null']},
                        'sacks_unassisted': {'type': ['number', 'null']},
                        'safeties': {'type': ['number', 'null']},
                        'tackle_yds': {'type': ['number', 'null']},
                        'tackles': {'type': ['number', 'null']},
                        'tackles_assisted': {'type': ['number', 'null']},
                        'tackles_for_loss_assisted': {'type': ['number', 'null']},
                        'tackles_for_loss_solo': {'type': ['number', 'null']},
                        'tackles_solo': {'type': ['number', 'null']},
                    },
                    'additionalProperties': False,
                },
                'special': {
                    'type': 'object',
                    'properties': {
                        'fc_yds': {'type': ['number', 'null']},
                        'fga1_19': {'type': ['number', 'null']},
                        'fga20_29': {'type': ['number', 'null']},
                        'fga30_39': {'type': ['number', 'null']},
                        'fga40_49': {'type': ['number', 'null']},
                        'fga50_59': {'type': ['number', 'null']},
                        'fga60': {'type': ['number', 'null']},
                        'fgm1_19': {'type': ['number', 'null']},
                        'fgm20_29': {'type': ['number', 'null']},
                        'fgm30_39': {'type': ['number', 'null']},
                        'fgm40_49': {'type': ['number', 'null']},
                        'fgm50_59': {'type': ['number', 'null']},
                        'fgm60': {'type': ['number', 'null']},
                        'field_goal_blocks_allowed': {'type': ['number', 'null']},
                        'field_goals': {'type': ['number', 'null']},
                        'field_goals_attempted': {'type': ['number', 'null']},
                        'field_goals_made': {'type': ['number', 'null']},
                        'fumble_return_pat': {'type': ['number', 'null']},
                        'kick_pat': {'type': ['number', 'null']},
                        'kick_return_pat': {'type': ['number', 'null']},
                        'kickoff_return_tds': {'type': ['number', 'null']},
                        'kickoff_return_yds': {'type': ['number', 'null']},
                        'kickoff_returns': {'type': ['number', 'null']},
                        'kickoff_touchbacks': {'type': ['number', 'null']},
                        'kickoff_yds': {'type': ['number', 'null']},
                        'kickoffs': {'type': ['number', 'null']},
                        'longest_fgm': {'type': ['number', 'null']},
                        'net_kickoff_yds': {'type': ['number', 'null']},
                        'net_punt_yds': {'type': ['number', 'null']},
                        'onside_attempts': {'type': ['number', 'null']},
                        'pass_2pt_att': {'type': ['number', 'null']},
                        'pass_2pt_conv': {'type': ['number', 'null']},
                        'pat_att': {'type': ['number', 'null']},
                        'punt_longest': {'type': ['number', 'null']},
                        'punt_return_tds': {'type': ['number', 'null']},
                        'punt_return_yds': {'type': ['number', 'null']},
                        'punt_returns': {'type': ['number', 'null']},
                        'punt_touchbacks': {'type': ['number', 'null']},
                        'punt_yds': {'type': ['number', 'null']},
                        'punts': {'type': ['number', 'null']},
                        'punts_inside_twenty': {'type': ['number', 'null']},
                        'receiving_pat': {'type': ['number', 'null']},
                        'redzone_end_field_goal': {'type': ['number', 'null']},
                        'redzone_end_fumble': {'type': ['number', 'null']},
                        'redzone_fg_made': {'type': ['number', 'null']},
                        'rush_2pt_att': {'type': ['number', 'null']},
                        'rush_pat': {'type': ['number', 'null']},
                        'successful_onside_kicks': {'type': ['number', 'null']},
                    },
                    'additionalProperties': False,
                },
            },
            'additionalProperties': False,
            'required': [
                'general',
                'offensive',
                'defensive',
                'special',
            ],
        },
    },
    'additionalProperties': False,
    'required' : [
        'meta',
        'stats',
        'pid',
    ],
}

BASEBALL = {
    'type': 'array',
    'items': {
        'type' : 'object',
        'properties' : {
            'pid': {'type': 'string', 'pattern': Patterns.ID},
            'meta': {
                'type': 'object',
                'properties': {
                    'class': {'type': ['number', 'null'], 'enum': [None,1,2,3,4,5]},
                    'conference': {'type': ['string', 'null']},
                    'date': {'type': ['number', 'null']}, # Unix time epoch (seconds since Jan 1, 1970)
                    'division': {'type': ['number', 'null'], 'enum': [None,1,2,3]},
                    'first': {'type': ['string', 'null']},
                    'institution': {'type': ['string', 'null']},
                    'last': {'type': ['string', 'null']},
                    'position': {'type': ['string', 'null'], 'enum': [None,'P','DH','INF','OF','C','IF']},
                    'sport': {'type': ['string', 'null'], 'const': Sports.BASEBALL},
                    'year': {'type': ['string', 'null'], 'pattern': Patterns.YEAR_RANGE},
                },
                'additionalProperties': False,
                'required': [
                    'class',
                    'conference',
                    'date',
                    'division',
                    'first',
                    'institution',
                    'last',
                    'position',
                    'sport',
                    'year',
                ],
            },
            'stats': {
                'type': 'object',
                'properties': {
                    'general': {
                        'type': 'object',
                        'properties': {
                            'games_played': {'type': ['number', 'null']},
                            'games_started': {'type': ['number', 'null']},
                        },
                        'additionalProperties': False,
                    },
                    'hitting': {
                        'type': 'object',
                        'properties': {
                            'batting_average': {'type': ['number', 'null']},
                            'on_base_percent': {'type': ['number', 'null']},
                            'slugging_percent': {'type': ['number', 'null']},
                            'runs': {'type': ['number', 'null']},
                            'at_bats': {'type': ['number', 'null']},
                            'hits': {'type': ['number', 'null']},
                            'doubles': {'type': ['number', 'null']},
                            'triples': {'type': ['number', 'null']},
                            'total_bases': {'type': ['number', 'null']},
                            'homeruns': {'type': ['number', 'null']},
                            'runs_batted_in': {'type': ['number', 'null']},
                            'walks': {'type': ['number', 'null']},
                            'hit_by_pitch': {'type': ['number', 'null']},
                            'sac_flys': {'type': ['number', 'null']},
                            'sac_hits': {'type': ['number', 'null']},
                            'strikeouts': {'type': ['number', 'null']},
                            'opposing_double_plays': {'type': ['number', 'null']}, # WTF is this?
                            'caught_stealing': {'type': ['number', 'null']},
                            'picked': {'type': ['number', 'null']},
                            'stolen_bases': {'type': ['number', 'null']},
                            'intentional_walks': {'type': ['number', 'null']},
                            'runs_batted_in_2_outs': {'type': ['number', 'null']},
                            'receptions_per_game': {'type': ['number', 'null']},
                        },
                        'additionalProperties': False,
                    },
                    'pitching': {
                        'type': 'object',
                        'properties': {
                            'appearances': {'type': ['number', 'null']},
                            'games_saved': {'type': ['number', 'null']},
                            'earned_runs': {'type': ['number', 'null']},
                            'earned_runs_average': {'type': ['number', 'null']},
                            'innings_pitched': {'type': ['number', 'null']},
                            'complete_games': {'type': ['number', 'null']},
                            'strikeouts': {'type': ['number', 'null']},
                            'shutouts': {'type': ['number', 'null']},
                            'batters_faced': {'type': ['number', 'null']},
                            'official_at_bats': {'type': ['number', 'null']},
                            'doubles_allowed': {'type': ['number', 'null']},
                            'triples_allowd': {'type': ['number', 'null']},
                            'balks': {'type': ['number', 'null']},
                            'homeruns_allowed': {'type': ['number', 'null']},
                            'wild_pitches': {'type': ['number', 'null']},
                            'hit_batters': {'type': ['number', 'null']},
                            'inherited_runs': {'type': ['number', 'null']},
                            'inherited_runs_scored': {'type': ['number', 'null']},
                            'sac_flys_allowed': {'type': ['number', 'null']},
                            'sac_hits_allowed': {'type': ['number', 'null']},
                            'pitches_thrown': {'type': ['number', 'null']},
                            'groundouts': {'type': ['number', 'null']},
                            'flyouts': {'type': ['number', 'null']},
                            'wins': {'type': ['number', 'null']},
                            'losses': {'type': ['number', 'null']},
                            'saves': {'type': ['number', 'null']},
                            'strikeouts_looking': {'type': ['number', 'null']},
                            'pickoffs': {'type': ['number', 'null']},
                        },
                        'additionalProperties': False,
                    },
                    'fielding': {
                        'type': 'object',
                        'properties': {
                            'putouts': {'type': ['number', 'null']},
                            'assists': {'type': ['number', 'null']},
                            'total_chances': {'type': ['number', 'null']},
                            'error': {'type': ['number', 'null']},
                            'fielding_percentage': {'type': ['number', 'null']},
                            'catcher_interferences': {'type': ['number', 'null']},
                            'passed_balls': {'type': ['number', 'null']},
                            'steal_attempts': {'type': ['number', 'null']},
                            'steals_caught': {'type': ['number', 'null']},
                            'infield_double_plays': {'type': ['number', 'null']},
                            'triple_plays': {'type': ['number', 'null']},
                        },
                        'additionalProperties': False,
                    },
                },
                'additionalProperties': False,
                'required': [
                    'general',
                    'hitting',
                    'pitching',
                    'fielding',
                ],
            },
        },
        'additionalProperties': False,
        'required' : [
            'meta',
            'stats',
            'pid',
        ],
    }
}
