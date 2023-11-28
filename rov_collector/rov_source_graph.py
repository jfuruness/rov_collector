import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from .enums_dataclasses import Source


class ROVSourceGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(self, out_dir: Optional[Path] = None) -> None:
        """Counts number of entries for each ASN and plots them"""

        source_counts = self._get_counts()

        # Sorting the sources based on counts in descending order
        sorted_sources_counts = sorted(
            source_counts.items(), key=lambda item: item[1], reverse=True
        )
        sources, counts = zip(*sorted_sources_counts)

        # Creating the bar graph
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sources, counts, color="skyblue")
        plt.xlabel("Source")
        plt.ylabel("Number of ASes")
        plt.title("Number of ASes per Source")
        plt.xticks(rotation=45)

        # Adding the count above each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                int(yval),
                va="bottom",
                ha="center",
            )

        dir_ = out_dir if out_dir else self.json_path.parent / "rov_source_counts.png"
        plt.savefig(dir_, bbox_inches="tight")
        plt.close()
        print(f"Saved to {dir_}")

    def _get_counts(self) -> dict[str, int]:
        counts = {x.value: 0 for x in list(Source)}
        with self.json_path.open() as f:
            data = json.load(f)
        for _, info_list in data.items():
            for inner_dict in info_list:
                counts[inner_dict["source"]] += 1
        return counts
