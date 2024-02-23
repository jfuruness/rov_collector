import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from ..enums_dataclasses import Source


class ROVSourceGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(self, out_path: Optional[Path] = None) -> None:
        """Counts number of entries for each ASN and plots them"""

        source_counts = self._get_counts()

        # Sorting the sources based on counts in descending order
        sorted_sources_counts = sorted(
            source_counts.items(), key=lambda item: item[1], reverse=True
        )
        sources, counts = zip(*sorted_sources_counts)

        category_counts = self._get_category_counts()

        # Creating the bar graph
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sources, counts, color="skyblue")

        # Find the index for Source.FRIENDS.value
        friends_index = sources.index(Source.FRIENDS.value)

        # Starting point for the first segment in the stacked bar
        bottom = 0

        # Iterate over category_counts and stack them on top of each other
        for category, count in category_counts.items():
            plt.bar(
                sources[friends_index],
                count,
                bottom=bottom,
                label=f"Category {category} ({count} ASes)",
            )
            bottom += count

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
                str(int(yval)),
                va="bottom",
                ha="center",
            )

        plt.legend()

        if not out_path:
            dir_ = self.json_path.parent / "rov_adoption_graphs"
            dir_.mkdir(parents=True, exist_ok=True)
            out_path = dir_ / "rov_source_counts.png"
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        print(f"Source counts saved to {out_path}")

    def _get_counts(self) -> dict[str, int]:
        counts = {x.value: 0 for x in list(Source)}
        counts["aggregate"] = 0
        with self.json_path.open() as f:
            data = json.load(f)
        for _, info_list in data.items():
            for inner_dict in info_list:
                counts[inner_dict["source"]] += 1
            counts["aggregate"] += 1
        return counts

    def _get_category_counts(self) -> dict[int, int]:
        """Gets counts for each category of ASes for Haya's sims

        Read their paper to understand (the friend's paper)
        """

        category_counts = {x: 0 for x in range(8)}

        with self.json_path.open() as f:
            data = json.load(f)
        for _, info_list in data.items():
            for inner_dict in info_list:
                if inner_dict["source"] == Source.FRIENDS.value:
                    category = int(inner_dict["metadata"]["category"])
                    category_counts[category] += 1
                    break
        # Remove any category_counts that are 0
        for k, v in category_counts.copy().items():
            if v == 0:
                del category_counts[k]

        return category_counts
