import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
from tqdm import tqdm

from bgpy.caida_collector import CaidaCollector


class ROVTierGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(self, out_dir: Optional[Path] = None) -> None:
        """Counts number of entries for each ASN and plots them"""

        as_topo = CaidaCollector().run()
        asn_group_counts = {k: 0 for k in as_topo.asn_groups}
        with self.json_path.open() as f:
            data = json.load(f)
            for asn in tqdm(data, total=len(data), desc="Counting groups"):
                for asn_group_key in asn_group_counts:
                    if int(asn) in as_topo.asn_groups[asn_group_key]:
                        asn_group_counts[asn_group_key] += 1
        # For the labels
        asn_group_percents = {
            k: f"{round(v * 100 / len(as_topo.asn_groups[k]))}%"
            for k, v in asn_group_counts.items()
        }

        x_vals = list(asn_group_counts.keys())
        y_vals = list(asn_group_counts.values())

        # Creating the bar graph
        plt.figure(figsize=(10, 6))
        bars = plt.bar(x_vals, y_vals, color="skyblue")
        plt.xlabel("Count by AS group")
        plt.ylabel("Number of ASes")
        plt.title("AS Group")
        plt.xticks(rotation=45)

        # Adding the count above each bar
        for bar, percent in zip(bars, asn_group_percents.values()):
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                percent,  # int(yval),
                va="bottom",
                ha="center",
            )

        dir_ = out_dir if out_dir else self.json_path.parent / "rov_group_counts.png"
        plt.savefig(dir_, bbox_inches="tight")
        plt.close()
        print(f"Saved to {dir_}")


if __name__ == "__main__":
    ROVTierGraph(Path.home() / "Desktop" / "rov_info.json").run()
