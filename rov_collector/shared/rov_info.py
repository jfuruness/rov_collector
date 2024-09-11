from dataclasses import dataclass
from typing import Any

from .enums import FilterType, Source


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
