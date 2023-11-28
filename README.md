[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
![Tests](https://github.com/jfuruness/rov_collector/actions/workflows/tests.yml/badge.svg)

# rov\_collector

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Credits](#credits)
* [History](#history)
* [Development/Contributing](#developmentcontributing)
* [Licence](#license)


## Package Description

This package downloads ROV data from a variety of sources and aggregates this information.
This is useful for simulations where you want to run mixed deployment scenarios
See the citations and explanations for all sources in the [Credits](#credits)
When the collectors are run, they output results into a JSON object.
This JSON is a dict where the key is ASN and the value is a list of ROVInfo objects

## Usage
* [rov\_collector](#rov\_collector)

from a script:

```python
from pathlib import Path

from rov_collector import rov_collector_classes
json_path: Path = Path.home() / "Desktop" / "rov_info.json"
for CollectorCls in rov_collector_classes:
    CollectorCls(json_path=json_path).run()
```

## Installation
* [rov\_collector](#rov\_collector)

Install python and pip if you have not already.

Then run:

```bash
pip3 install pip --upgrade
pip3 install wheel
```

For production:

```bash
pip3 install rov_collector
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/rov_collector.git
cd rov_collector
pip3 install -e .[test]
pre-commit install
```

To test the development package: [Testing](#testing)


## Testing
* [rov\_collector](#rov\_collector)

To test the package after installation:

```
cd rov_collector
pytest rov_collector
ruff rov_collector
black rov_collector
mypy rov_collector
```

If you want to run it across multiple environments, and have python 3.10 and 3.11 installed:

```
cd rov_collector
tox
```

## Credits
* [rov\_collector](#rov\_collector)

#### Revisiting RPKI Route Origin Validation on the Data Plane

Explanation:

We recieved the data source from this paper through email from from Mar 22, 2022 from Matthias Waehlisch <m.waehlisch@fu-berlin.de>

When the CSV says strong confidence, this indicates that it is 1 hop from PEERING.
When the CSV days weak confidence, that indicates that is 2+ hops from PEERING

Paper URL: [URL](https://tma.ifip.org/2021/wp-content/uploads/sites/10/2021/08/tma2021-paper11.pdf)

Paper data sources: [github](https://github.com/nrodday/TMA-21)

Bibtex:

```
@inproceedings{RoddayCBKRSW21,
  title = {Revisiting RPKI Route Origin Validation on the Data Plane},
  author = {Nils Rodday and Ítalo S. Cunha and Randy Bush and Ethan Katz-Bassett and Gabi Dreo Rodosek and Thomas C. Schmidt and Matthias Wählisch},
  year = {2021},
  url = {http://dl.ifip.org/db/conf/tma/tma2021/tma2021-paper11.pdf},
  researchr = {https://researchr.org/publication/RoddayCBKRSW21},
  cites = {0},
  citedby = {0},
  booktitle = {5th Network Traffic Measurement and Analysis Conference, TMA 2021, Virtual Event, September 14-15, 2021},
  editor = {Vaibhav Bajpai and Hamed Haddadi and Oliver Hohlfeld},
  publisher = {IFIP},
  isbn = {978-3-903176-40-9},
}
```

Github links:
* [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/tma_collector.py)
* [emailed CSV](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/data/tma.csv)

## History
* [rov\_collector](#rov\_collector)

TODO

## Development/Contributing
* [rov\_collector](#rov\_collector)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Test it
5. Run tox
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com if it's been a while and I haven't seen it

## License
* [rov\_collector](#rov\_collector)

BSD License (see license file)
