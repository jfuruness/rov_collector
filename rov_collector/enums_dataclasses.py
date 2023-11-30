from dataclasses import dataclass
from enum import Enum
from typing import Any


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


@dataclass
class ROVInfo:
    """ROV Info about any given AS that is JSON serializable"""

    asn: int
    filter_type: FilterType
    percent: float
    source: Source
    metadata: dict[Any, Any]

    def to_json(self):
        return {
            "asn": str(self.asn),
            "filter_type": self.filter_type.value,
            "percent": str(self.percent),
            "source": self.source.value,
            "metadata": self.metadata,
        }
