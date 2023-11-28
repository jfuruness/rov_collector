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
See the citations for all sources in the [Credits](#credits)

## Usage
* [rov\_collector](#rov\_collector)

from a script:

```python
from pathlib import Path

from rov_collector import ROVCollector

json_path = Path("/tmp/my_json_path.json")  # or set to None to avoid writing
JSONCollector(json_path).run(graph=True)
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

TODO

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
