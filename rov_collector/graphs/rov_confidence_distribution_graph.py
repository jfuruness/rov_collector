import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from ..enums_dataclasses import Source


class ROVConfidenceDistributionGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(self, out_dir: Optional[Path] = None) -> None:
        """Counts number of entries for each ASN and plots them"""

        if not out_dir:
            out_dir = self.json_path.parent / "rov_adoption_graphs"
        out_dir.mkdir(parents=True, exist_ok=True)

        source_data_dict = self._get_source_data_dict()
        self._plot_single_sources(source_data_dict, out_dir)
        self._plot_all_sources(source_data_dict, out_dir)

        print(f"distribution saved to {out_dir}")

    def _get_source_data_dict(self) -> dict[str, list[float]]:
        """Reads JSON and returns data dict of {source: [99, 87, 1, ...]}"""
        # Sources that don't include a percent

        data: dict[str, list[float]] = {x.value: list() for x in list(Source)}
        with self.json_path.open() as f:
            for asn, inner_list in json.load(f).items():
                for item in inner_list:
                    data[item["source"]].append(float(item["percent"]))

        no_conf_sources = [Source.IS_BGP_SAFE_YET, Source.FRIENDS, Source.TMA]
        for source in no_conf_sources:
            del data[source.value]
        return data

    def _plot_single_sources(
        self, source_data_dict: dict[str, list[float]], out_dir: Path
    ) -> None:
        """Plot single data sources"""

        for source, percents in source_data_dict.items():
            percents.sort(reverse=True)  # descending
            plt.figure()
            plt.scatter(range(len(percents)), percents)
            plt.title(f"ROV Confidence For {source}")
            plt.xlabel("Index")
            plt.ylabel("Percent")
            plt.grid(True)
            plt.savefig(
                out_dir / f"{source}_rov_confidence_distribution.png",
                bbox_inches="tight",
            )
            plt.close()

    def _plot_all_sources(
        self, source_data_dict: dict[str, list[float]], out_dir: Path
    ) -> None:
        """Plot all sources"""

        # Create an aggregate scatter plot
        plt.figure()
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        assert len(colors) >= len(list(Source))

        for i, (source, percents) in enumerate(source_data_dict.items()):
            plt.scatter(range(len(percents)), percents, color=colors[i], label=source)

        plt.title("ROV Confidence For All Sources")
        plt.xlabel("Index")
        plt.ylabel("Percent")
        plt.legend()
        plt.grid(True)
        plt.savefig(
            out_dir / "all_rov_confidence_distribution.png", bbox_inches="tight"
        )
        plt.close()
