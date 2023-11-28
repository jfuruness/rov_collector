import csv
from dataclasses import asdict
from pathlib import Path
import re
from typing import Any, Optional

import requests

from .roa import ROA


class ROACollector:
    """This class downloads, and stores ROAs from rpki validator"""

    URL: str = "https://rpki-validator.ripe.net/api/export.json"

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path: Optional[Path] = csv_path

    def run(self) -> tuple[ROA, ...]:
        """Downloads and stores roas from a json"""

        roas = self._parse_roa_json(self._get_json_roas())
        self._write_csv(roas)
        return roas

    def _get_json_roas(self) -> list[dict[Any, Any]]:
        """Returns the json from the url for the roas"""

        headers = {"Accept": "application/xml;q=0.9,*/*;q=0.8"}
        response = requests.get(self.URL, headers=headers)
        response.raise_for_status()
        roas_list = response.json()["roas"]
        assert isinstance(roas_list, list), "(for mypy) not a list? {roas_list}"
        return roas_list

    def _parse_roa_json(
        self, unformatted_roas: list[dict[Any, Any]]
    ) -> tuple[ROA, ...]:
        """Parse JSON into a tuple of ROA objects"""

        formatted_roas = []
        for roa in unformatted_roas:
            formatted_roas.append(
                ROA(
                    asn=int(re.findall(r"\d+", roa["asn"])[0]),
                    prefix=roa["prefix"],
                    max_length=int(roa["maxLength"]),
                    # RIPE, afrinic, etc
                    ta=roa["ta"],
                )
            )
        return tuple(formatted_roas)

    def _write_csv(self, roas: tuple[ROA, ...]) -> None:
        """Writes ROAs to a CSV if csv_path is not None"""

        if self.csv_path:
            with self.csv_path.open("w") as temp_csv:
                fieldnames = list(asdict(roas[0]).keys())
                writer = csv.DictWriter(temp_csv, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([asdict(x) for x in roas])
