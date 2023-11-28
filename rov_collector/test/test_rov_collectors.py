import json
from pathlib import Path
from typing import Any

import pytest

from rov_collector import rov_collector_classes


class TestROVCollector:
    """Tests ROV Collectors

    I know this needs more in depth testing, but this will do for now
    """

    @pytest.mark.parametrize("ROVCollectorCls", rov_collector_classes)
    def test_rov_collector(self, ROVCollectorCls, tmp_path):
        """System test for the ROV Collector"""

        json_path = tmp_path / "test.json"

        dummy_entry = self._save_dummy_entry(json_path)

        collector = ROVCollectorCls(
            json_path=json_path, requests_cache_db_path=tmp_path / "requests_cache.db"
        )
        # Ensure ROV info is gathered
        rov_info = collector._collect_rov_info()
        assert len(rov_info) > 1, "No ROV Info?"

        # Run collector, which should dump to a JSON
        collector.run()
        with json_path.open() as f:
            json_rov_info = json.load(f)

        # Ensure items in the JSON are the same as non JSON
        for asn, rov_info_list in rov_info.items():
            json_rov_info_list = json_rov_info[str(asn)]
            jsonified_rov_info_list = [x.to_json() for x in rov_info_list]
            assert json_rov_info_list == jsonified_rov_info_list

        # Add 1 to account for manually added entry
        assert len(json_rov_info) == len(rov_info) + 1
        # Make sure old JSON wasn't deleted
        assert json_rov_info[self._dummy_asn_str] == dummy_entry[self._dummy_asn_str]

    def _save_dummy_entry(self, json_path: Path) -> dict[Any, Any]:
        """Saves dummy entry in json and returns dummy entry"""

        with json_path.open("w") as f:
            dummy_entry = self._get_dummy_entry()
            json.dump(dummy_entry, f, indent=4)
            return dummy_entry

    def _get_dummy_entry(self) -> dict[Any, Any]:
        return {
            self._dummy_asn_str: [
                {
                    # Pick a number that will never be used lol
                    "asn": self._dummy_asn_str,
                    "filter_type": "unknown",
                    "percent": "1",
                    "source": "dummy",
                    "metadata": {"test": "test"},
                }
            ]
        }

    @property
    def _dummy_asn_str(self) -> str:
        """Returns a dummy ASN string that no one will ever use"""
        return "1" * 20
