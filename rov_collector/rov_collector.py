import json
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path

import requests_cache

from .shared import DIRS, SINGLE_DAY_CACHE_DIR, ROVInfo


class ROVCollector(ABC):
    """Abstract class for downloading ROV data"""

    def __init__(
        self,
        json_path: Path = Path(DIRS.user_desktop_dir) / "rov_info.json",
        requests_cache_db_path: Path | None = None,
    ):
        self.json_path: Path = json_path

        # By default keep requests cached for a single day
        if requests_cache_db_path is None:
            requests_cache_db_path = SINGLE_DAY_CACHE_DIR / "requests_cache.db"
        self.requests_cache_db_path: Path = requests_cache_db_path
        self.session = requests_cache.CachedSession(str(self.requests_cache_db_path))

    def __del__(self):
        self.session.close()

    def run(self) -> None:
        """Download ROV data w/cached requests, add to old JSON file"""

        # Get new ROV info
        new_rov_info = self._collect_rov_info()

        # Read in old ROV info
        if self.json_path.exists():
            with self.json_path.open() as f:
                rov_info = json.load(f)
        else:
            rov_info = dict()

        # Add new ROV info to the dictionary
        for asn, rov_info_list in new_rov_info.items():
            rov_info_list_json = [x.to_json() for x in rov_info_list]
            rov_info[str(asn)] = rov_info.get(str(asn), list()) + rov_info_list_json

        # Save the dictionary to a JSON
        with self.json_path.open("w") as f:
            json.dump(rov_info, f, indent=4)

    @abstractmethod
    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        raise NotImplementedError

    @property
    def data_dir(self) -> Path:
        return Path(__file__).parent / "data"
