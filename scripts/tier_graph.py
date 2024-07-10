from functools import partial
import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
from tqdm import tqdm

from bgpy.as_graphs import CAIDAASGraphConstructor

from rov_collector import Source


plt.rcParams["font.size"] = 18


NOOP = lambda x: True

class ROVTierGraph:
    def __init__(self, json_path: Path) -> None:
        self.json_path: Path = json_path

    def run(
        self,
        as_topo,
        out_dir: Optional[Path] = None,
        allowed_rov_sources=frozenset([x.value for x in Source]),
        fits_extra_reqs_func=NOOP,
    ) -> None:
        """Counts number of entries for each ASN and plots them"""

        asn_group_counts = {k: 0 for k in as_topo.asn_groups}
        with self.json_path.open() as f:
            data = json.load(f)
            for asn, info_list in tqdm(
                data.items(), total=len(data), desc="Counting groups"
            ):
                if any(
                    x["source"] in allowed_rov_sources and float(x["percent"]) > 0
                    and fits_extra_reqs_func(x)
                    for x in info_list
                ):
                    for asn_group_key in asn_group_counts:
                        if int(asn) in as_topo.asn_groups[asn_group_key]:
                            asn_group_counts[asn_group_key] += 1

        # Formatting for papers
        del asn_group_counts["ixp"]
        del asn_group_counts["stub_or_multihomed"]
        del asn_group_counts["etc"]

        # For the labels
        asn_group_percents = {
            # k: f"{round(v * 100 / len(as_topo.asn_groups[k]))}%"
            k: v * 100 / len(as_topo.asn_groups[k])
            for k, v in asn_group_counts.items()
        }

        asn_group_counts["all"] = asn_group_counts["all_wout_ixps"]
        del asn_group_counts["all_wout_ixps"]
        asn_group_percents["all"] = asn_group_percents["all_wout_ixps"]
        del asn_group_percents["all_wout_ixps"]

        asn_group_counts["tier-1"] = asn_group_counts["input_clique"]
        del asn_group_counts["input_clique"]
        asn_group_percents["tier-1"] = asn_group_percents["input_clique"]
        del asn_group_percents["input_clique"]

        asn_group_percents = {
            k: v for k, v in sorted(asn_group_percents.items(), key=lambda x: x[1])
        }
        asn_group_counts = {k: asn_group_counts[k] for k in asn_group_percents}

        x_vals = list(asn_group_percents.keys())
        y_vals = list(asn_group_percents.values())

        # Creating the bar graph
        plt.figure(figsize=(10, 6))
        bars = plt.bar(x_vals, y_vals, color="skyblue")
        plt.xlabel("Count by AS group")
        plt.ylabel("Percent of ASes")
        plt.title("AS Group")
        plt.xticks(rotation=45)

        # Adding the count above each bar
        for bar, count in zip(bars, asn_group_counts.values()):
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                count,  # int(yval),
                va="bottom",
                ha="center",
            )

        default_name = f"{'_'.join(allowed_rov_sources)}".replace(" ", "_")
        if fits_extra_reqs_func != NOOP:
            default_name += "_" + getattr(fits_extra_reqs_func, "__name__", "")
        default_name += ".png"
        default_path = self.json_path.parent / "rov_group_counts" / default_name
        dir_ = out_dir if out_dir else default_path
        plt.savefig(dir_, bbox_inches="tight")
        plt.close()
        print(f"Saved to {dir_}")


def fits_categories(x, categories: tuple[int, ...]) -> bool:
    return int(x["metadata"].get("category")) in categories


fits_categories_367 = partial(fits_categories, categories=(3, 6, 7))
fits_categories_367.__name__ = "categories_367"  # type: ignore


if __name__ == "__main__":
    in_path = Path.home() / "Desktop" / "rov_info.json"

    as_topo = CAIDAASGraphConstructor(tsv_path=None).run()
    ROVTierGraph(in_path).run(as_topo)
    # Friends paper with only categories 3, 6, 7
    ROVTierGraph(in_path).run(
        as_topo,
        allowed_rov_sources=frozenset([Source.FRIENDS.value]),
        fits_extra_reqs_func=fits_categories_367,
    )
    for source in Source:
        ROVTierGraph(in_path).run(as_topo, allowed_rov_sources=frozenset([source.value]))
