from collections import defaultdict
import re
from typing import Any

from tqdm import tqdm

from rov_collector.enums_dataclasses import FilterType, ROVInfo, Source
from rov_collector.rov_collector import ROVCollector


class APNICCollector(ROVCollector):
    """Downloads ROV data for 'https://rovista.netsecurelab.org/' (source in README)"""

    URL: str = "https://stats.labs.apnic.net/"

    def _collect_rov_info(self) -> defaultdict[int, list[ROVInfo]]:
        """Downloads and parses ROV info"""

        rov_info: defaultdict[int, list[ROVInfo]] = defaultdict(list)

        all_ases = set()
        for row in self._get_website_rows():
            # Add ROV data
            asn = int(row["asn"])
            if asn in all_ases:
                continue
            all_ases.add(asn)

            percent = float(row["percent"])
            # Only take ASes deploying ROV
            if percent != 0:
                rov_info[asn].append(
                    ROVInfo(
                        asn=asn,
                        filter_type=FilterType.UNKNOWN,
                        percent=percent,
                        source=Source.APNIC,
                        metadata=row,
                    )
                )
        return rov_info

    def _get_website_rows(self) -> list[dict[str, str]]:
        """Downloads website JSON from API

        First gets the URLs for the table on the homepage
        Then for each URL, download the ASNs and corresponding data
        """

        rows = list()
        urls = self._get_main_page_urls()
        for url in tqdm(urls, total=len(urls), desc="Parsing APNIC URLs"):
            rows.extend(self._download_parse_country_url(url))
        return rows

    def _get_main_page_urls(self) -> tuple[str, ...]:
        """Downloads the main page, and gets all URLs for corresponding links

        of course it uses javascript. of course.
        """

        relevant_lines = self._get_relevant_lines(
            url=self.URL + "rpki",
            start_line_str="['CC', 'Country',",
            end_line_str="]);",
        )

        urls = list()
        for line in relevant_lines:
            matches = re.findall(r'.*<a href=\\"/(rpki/..)\\">..</a>.*', line)
            assert len(matches) == 1, matches
            urls.append(self.URL + matches[0])
        return tuple(urls)

    def _get_relevant_lines(
        self, url: str, start_line_str: str, end_line_str: str
    ) -> list[str]:
        """Returns relevant lines for regex, since we can't use bs4 due to js"""

        resp = self.session.get(url)
        resp.raise_for_status()
        with open("/tmp/resp.html", "w") as f:
            f.write(resp.text)

        relevant_lines = list()
        started = False
        for line in resp.text.split("\n"):
            if end_line_str in line and started:
                break
            if started:
                relevant_lines.append(line)
            if start_line_str in line:
                started = True
        resp.close()
        return relevant_lines

    def _download_parse_country_url(self, url: str) -> list[dict[Any, Any]]:
        """Downloads a specific countrie's URL and parses ASN table"""

        relevant_lines = self._get_relevant_lines(url, "ASN", "]);")

        data = list()
        for line in relevant_lines:
            # Get ASN
            matches = re.findall(r">(AS\d+)<", line)
            # Sometimes AS is the name, in which case, three matches
            assert len(matches) in [1], line
            asn = int(matches[0].replace("AS", ""))

            # Get percent
            matches = re.findall(r"'(.*)%'", line)
            if len(matches) == 1:
                percent = float(matches[0])
                if percent == 0:
                    continue
            # not adopting
            elif len(matches) == 0:
                continue
            else:
                raise NotImplementedError(f"Case not accounted for {line}")

            data.append({"asn": asn, "percent": percent})
        return data
