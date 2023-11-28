import csv
from dataclasses import asdict


from roa_collector import ROACollector


class TestROACollector:
    """Tests ROA Collector

    I know this needs more in depth testing, but this will do for now
    """

    # NOTE: no point in parametrizing. Doubles runtime of test, and
    # might as well just test all branches at once since it's a system test
    # and I'm just trying to do this quickly
    def test_roa_collector(self, tmp_path, write_csv=True):
        """System test for the ROA Collector"""

        csv_path = tmp_path / "test.csv"
        roas = ROACollector(csv_path).run()
        assert len(roas) > 100, "Not enough ROAs returned?"
        if write_csv:
            with csv_path.open() as f:
                for row, roa in zip(csv.DictReader(f), roas):
                    assert row == {k: str(v) for k, v in asdict(roa).items()}
