from cloudscout_rest.schemas.enums import Patterns

class SchemaObject:
    """
    Base class for wrapping JSON-schema representations.
    """
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

    def raw(self):
        raise NotImplementedError

class StatSchema(SchemaObject):
    """
    Description:
    ============

    Wrapper for a JSON-schema representation. The purpose of this class in
    specific is to make defining player statistics simpler and reduce repetitve
    definitions.

    Example:
    ========
    
    >> SchemaObject('general', ['games_played', 'games_started']).raw()
    {
        'type': 'object',
        'properties': {
            'games_played': {'type': ['number', 'null']},
            'games_started': {'type': ['number', 'null']}
        },
        'additionalProperties': False,
        'required': [
            'games_played',
            'games_started'
        ]
    }
    """
    def raw(self):
        # all stats are numbers and are nullable
        num_schema = {'type': ['number', 'null']}
        schema = {
            'type': 'object',
            'properties': {prop:num_schema for prop in self.properties},
            'additionalProperties': False,
            'required': [prop for prop in self.properties]
        }
        return schema

class PlayerSchema(SchemaObject):
    """
    Description:
    ============

    Wrapper for a JSON-schema representation. The purpose of this class in
    specific is to make defining player objects simpler and reduce repetitve
    definitions. Each player has the schema defined in the 'raw()' method in
    common.
    """
    def __init__(self, sport, properties):
        self.sport = sport.value
        super().__init__(self.sport.name, properties)

    def raw(self):
        schema = {
            'type': 'object',
            'properties': {
                'pid': {'type': 'string', 'pattern': ''},
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
                        'position': {'type': ['string', 'null'], 'enum': [None] + self.sport.positions},
                        # include gender?
                        'sport': {'type': ['string', 'null'], 'const': self.sport.name},
                        'year': {'type': ['string', 'null'], 'pattern': Patterns.YEAR_RANGE.value},
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
                    ]
                },
                'stats': {
                    'type': 'object',
                    'properties': {prop.name:prop.raw() for prop in self.properties},
                    'additionalProperties': False,
                    'required': [prop.name for prop in self.properties]
                }
            },
            'additionalProperties': False,
            'required': ['pid', 'meta', 'stats']
        }
        return schema
