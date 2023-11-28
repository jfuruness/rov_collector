from pathlib import Path

from .collectors import rov_collector_classes


def main():
    json_path: Path = Path.home() / "Desktop" / "rov_info.json"
    for CollectorCls in rov_collector_classes:
        CollectorCls(json_path=json_path).run()


if __name__ == "__main__":
    main()
