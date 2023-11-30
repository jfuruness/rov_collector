from collections import defaultdict
import json
from pathlib import Path

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class FriendsCollector(ROVCollector):
    """Downloads ROV data for 'friends' paper (source in README)

    I ran the jupyter notebook in the paper, and with 8.95% failed
    connections, I got this dataset that is saved in the jSON
    """

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        # Open CSV
        with self.json_source_path.open() as f:
            data = json.load(f)
        for category, as_list in data.items():
            # ROV evidence, and STRONG evidence
            if category in ["2", "3", "6", "7"]:
                for asn in as_list:
                    # Negative ASNs are that of IXPs
                    if int(asn) > 0:
                        rov_info[int(asn)].append(
                            ROVInfo(
                                asn=int(asn),
                                # No info on peering vs all
                                filter_type=FilterType.UNKNOWN,
                                percent=100,
                                source=Source.FRIENDS,
                                metadata={"category": int(category)},
                            )
                        )
        return rov_info

    @property
    def json_source_path(self) -> Path:
        return self.data_dir / "friends.json"
