from pathlib import Path

from rov_collector import rov_collector_classes
from rov_collector import ROVSourceGraph


def main():
    json_path: Path = Path.home() / "Desktop" / "rov_info.json"
    # Clear out old files, since by default the collectors append
    json_path.unlink(missing_ok=True)
    for CollectorCls in rov_collector_classes:
        # For some reason mypy is freaking out about the instantiation here
        CollectorCls(json_path=json_path).run()  # type: ignore
    ROVSourceGraph(json_path).run()


if __name__ == "__main__":
    main()
