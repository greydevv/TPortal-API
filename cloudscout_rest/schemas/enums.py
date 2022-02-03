from enum import Enum
from dataclasses import dataclass
from typing import List

@dataclass
class SportData:
    name: str
    positions: List[str]

class Patterns(Enum):
    USER_ID = r'^[0-9a-z]+$'
    ID = r'^[0-9]{10}$'
    EMAIL = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    YEAR_RANGE = r'^[0-9]{2}-[0-9]{2}$'

class Sports(Enum):
    FOOTBALL = SportData('FOOTBALL', ['QB', 'WR', 'OL', 'RB', 'TE', 'C', 'OT', 'FB', 'DL', 'DT', 'DE', 'LB', 'DB', 'CB', 'S', 'P', 'K', 'LS'])
    BASEBALL = SportData('BASEBALL', ['P', 'C', 'INF', 'OF', 'UT', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH'])
    BASKETBALL = SportData(['MENS_BASKETBALL', 'WOMENS_BASKETBALL'], ['F', 'G', 'C'])
    HOCKEY = SportData(['MENS_ICE_HOCKEY', 'WOMENS_ICE_HOCKEY'], ['G', 'D', 'F'])
    SOCCER = SportData(['MENS_SOCCER', 'WOMENS_SOCCER'], ['GK', 'D', 'M', 'F'])
    LACROSSE = SportData(['MENS_LACROSSE', 'WOMENS_LACROSSE'], ['M', 'FO', 'DM', 'ATT', 'D', 'M', 'GK'])
    VOLLEYBALL = SportData(['MENS_VOLLEYBALL', 'WOMENS_VOLLEYBALL'], ['L', 'MB', 'OH', 'OPP', 'S'])
    FIELD_HOCKEY = SportData('FIELD_HOCKEY', ['M', 'GK', 'F', 'B'])
    SOFTBALL = SportData('SOFTBALL', ['C', 'INF', 'OF', 'SP/RP', 'UT'])
