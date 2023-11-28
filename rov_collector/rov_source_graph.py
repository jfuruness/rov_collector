import json
from pathlib import Path

import matplotlib.pyplot as plt

from .enums_dataclasses import Source


class ROVSourceGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(self) -> None:
        """Counts number of entries for each ASN and plots them"""

        source_counts = self._get_counts()
        sources = list(source_counts.keys())
        counts = list(source_counts.values())

        # Creating the bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(sources, counts, color="skyblue")
        plt.xlabel("Source")
        plt.ylabel("Number of ASes")
        plt.title("Number of ASes per Source")
        plt.xticks(rotation=45)
        plt.show()

    def _get_counts(self) -> dict[str, int]:
        counts = {x.value: 0 for x in list(Source)}
        with self.json_path.open() as f:
            data = json.load(f)
        for _, info_list in data.items():
            for inner_dict in info_list:
                counts[inner_dict["source"]] += 1
        return counts
