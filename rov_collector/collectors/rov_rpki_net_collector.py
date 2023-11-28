from collections import defaultdict
import json
from pathlib import Path

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class ROVRPKINetCollector(ROVCollector):
    """Downloads ROV data for 'rov.rpki.net' (source in README)"""

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        # Open CSV
        with self.json_source_path.open() as f:
            data = json.load(f)
        for as_info in data:
            # Add ROV data
            asn = int(as_info["asn"])
            # Not sure what these are, but I've reverse engineered that the latest
            # entry in this list is what's used as the ROV Confidence on the website
            vps = list(sorted(as_info["vps"], key=lambda x: x["last_measured"]))
            assert vps
            percent = vps[-1]["confidence"]
            if float(percent) >= 0:
                rov_info[asn].append(
                    ROVInfo(
                        asn=asn,
                        # No info on peering vs all
                        filter_type=FilterType.UNKNOWN,
                        percent=percent * 100,
                        source=Source.ROV_RPKI_NET,
                        metadata=as_info,
                    )
                )

        return rov_info

    @property
    def json_source_path(self) -> Path:
        return self.data_dir / "rov.rpki.net.json"
