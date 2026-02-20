from enum import Enum

class GeoSite(Enum):
    MANDAL = 'M'
    BLOCK = 'B'
    VILLAGE = 'V'
    DISTRICT = 'D'
    STATE = 'S'
    COUNTRY = 'C'