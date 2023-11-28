from pathlib import Path

from .collectors import rov_collector_classes


def main():
    json_path: Path = Path.home() / "Desktop" / "rov_info.json"
    for CollectorCls in rov_collector_classes:
        # For some reason mypy is freaking out about the instantiation here
        CollectorCls(json_path=json_path).run()  # type: ignore


if __name__ == "__main__":
    main()
