from collections import defaultdict
import csv
from pathlib import Path

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class TMACollector(ROVCollector):
    """Downloads ROV data for 'Revisiting RPKI... (source in README)"""

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        # Open CSV
        with self.csv_path.open() as f:
            reader = csv.DictReader(f, delimiter="-")
            reader.fieldnames = [x.strip() for x in reader.fieldnames]  # type: ignore
            for row in reader:
                # Add ROV data
                asn = int(row["asn"].strip())
                rov_info[asn].append(
                    ROVInfo(
                        asn=asn,
                        filter_type=FilterType.UNKNOWN,
                        # There is only strong or weak, the percents are arbitrary
                        percent=100 if "strong" in row["confidence"] else 50,
                        source=Source.TMA,
                        metadata=dict(row),
                    )
                )

        return rov_info

    @property
    def csv_path(self) -> Path:
        return self.data_dir / "tma.csv"
