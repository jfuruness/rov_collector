from collections import defaultdict
import csv
from io import StringIO

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class IsBGPSafeYetCollector(ROVCollector):
    """Downloads ROV data for 'Revisiting RPKI... (source in README)"""

    URL = (
        "https://raw.githubusercontent.com/cloudflare/isbgpsafeyet.com/"
        "master/data/operators.csv"
    )

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        for row in self._get_csv_rows():
            # Add ROV data
            asn = int(row["asn"].strip())

            if "filtering peers only" in str(row["details"]):
                filter_type = FilterType.PEERS
            elif "filtering" in str(row["details"]):
                filter_type = FilterType.ALL
            elif "unsafe" in row["status"]:
                # Not filtering
                continue
            else:
                raise NotImplementedError("Case not accounted for")

            rov_info[asn].append(
                ROVInfo(
                    asn=asn,
                    filter_type=filter_type,
                    # There is only strong or weak, the percents are arbitrary
                    percent=1,
                    source=Source.IS_BGP_SAFE_YET,
                    metadata={k: v for k, v in dict(row).items() if k != "asn"},
                )
            )

        return rov_info

    def _get_csv_rows(self) -> list[dict[str, str]]:
        """Downloads CSV from isbgpsafeyet.com and returns rows of CSV"""

        resp = self.session.get(self.URL)
        resp.raise_for_status()
        # Treat the string as a file
        csv_file = StringIO(resp.text)
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        csv_file.close()
        resp.close()
        input(rows[:5])
        return rows
