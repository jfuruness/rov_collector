from dataclasses import dataclass


@dataclass(frozen=True)
class ROA:
    asn: int
    prefix: str
    max_length: int
    # RIPE, afrinic, etc (ta comes from the JSON)
    ta: str
