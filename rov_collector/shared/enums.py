from enum import Enum


class FilterType(Enum):
    """Whether ROV is filtering all ASes, only peers, or unknown"""

    ALL = "all"
    PEERS = "peers"
    UNKNOWN = "unknown"


class Source(Enum):
    """Source for ROV data

    (see README for credits)
    """

    TMA = "Revisiting RPKI"
    IS_BGP_SAFE_YET = "isbgpsafeyet"
    ROV_RPKI_NET = "rov.rpki.net"
    ROVISTA = "ROVISTA"
    APNIC = "APNIC"
    FRIENDS = "Friends"
