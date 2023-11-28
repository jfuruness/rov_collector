from collections import defaultdict

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class ROVISTACollector(ROVCollector):
    """Downloads ROV data for 'https://rovista.netsecurelab.org/' (source in README)"""

    URL: str = "https://api.rovista.netsecurelab.org/rovista/api/overview"

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        for row in self._get_website_rows():
            # Add ROV data
            asn = int(row["asn"])
            # Only take ASes deploying ROV
            if float(row["ratio"]) != 0:
                rov_info[asn].append(
                    ROVInfo(
                        asn=asn,
                        filter_type=FilterType.UNKNOWN,
                        percent=float(row["ratio"]),
                        source=Source.ROVISTA,
                        metadata=dict(row),
                    )
                )

        return rov_info

    def _get_website_rows(self) -> list[dict[str, str]]:
        """Downloads website JSON from API

        NOTE: the API offset doesn't work after a certain number
        So instead you just need to download it in one giant batch
        """

        headers = {"accept": "application/json"}

        params = {
            "offset": "0",
            # See func docstr
            "count": "1000000",
            "sortBy": "rank",
            "sortOrder": "asc",
        }
        resp = self.session.get(self.URL, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # see func docstr
        assert data["itemCount"] >= data["totalCount"]
        resp.close()
        assert isinstance(data["data"], list), "for mypy"
        assert all(isinstance(x, dict) for x in data["data"]), "for mypy"
        return data["data"]
