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

The results of a run from Nov 30 2023 can be seen here. Additionally, from the "Friends" paper, it's important to note that category 4 and category 5 ASes are not considered as ROV adopting, but are included in the graph for clarity.
![Image](https://drive.google.com/uc?export=view&id=1JxbyrKyGVKvNwUazSr_7sU_xijF5WUqK)
![Image](https://drive.google.com/uc?export=view&id=1c_x8EkkZ05YXjWf0yzlgs5z2ECQitIDS)


## Usage
* [rov\_collector](#rov\_collector)

from a script:

```python
from pathlib import Path

from rov_collector import rov_collector_classes


def main():
    json_path: Path = Path.home() / "Desktop" / "rov_info.json"
    # Clear out old files, since by default the collectors append
    json_path.unlink(missing_ok=True)
    for CollectorCls in rov_collector_classes:
        # For some reason mypy is freaking out about the instantiation here
        CollectorCls(json_path=json_path).run()  # type: ignore


if __name__ == "__main__":
    main()
```

From the command line:

```
rov_collector
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
@inproceedings{mixed_deployment_3,
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

#### Cloudflare's isbgpsafeyet.com

Explanation:

This site by cloudflare allows you to test your ISP for ROV safety and stores this info.
They also defined whether it filters all ASes or only peers

Paper URL: [URL](https://isbgpsafeyet.com/)

Paper data sources: [github](https://github.com/cloudflare/isbgpsafeyet.com/)

Bibtex:

```
@misc{mixed_deployment_1,
  title = {Is BGP Safe Yet?},
  author = {Cloudflare},
  url = {https://isbgpsafeyet.com/},
  year = {2023},
}
```

Github links:
* [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/is_bgp_safe_yet_collector.py)
* [CSV](https://raw.githubusercontent.com/cloudflare/isbgpsafeyet.com/master/data/operators.csv)

#### Measuring RPKI Route Origin Validation Deployment

Explanation:

At the time of publication this was one of the largest data sources for ROV ASes.
They also had a nice website listing out all the ROV AS data.
The website was last updated in 2020, so I'm not worried about a live feed.
Instead I've just right clicked inspect on their page using google chrome,
then clicked on the network tab,
reloaded the page,
and clicked on the asn query,
and then clicked on response,
and copy pasted this locally.
I've checked that it's the same as the page.

Paper URL: [URL](https://rov.rpki.net/paper)

Paper data sources: [github](https://github.com/RPKI/rov-measurement-code), [website](https://rov.rpki.net/)

Bibtex:

```
@article{mixed_deployment_2,
title={Towards a rigorous methodology for measuring adoption of rpki route validation and filtering},
author={Reuter, Andreas and Bush, Randy and Cunha, It{^a}lo and Katz-Bassett, Ethan and Schmidt, Thomas C and W{"a}hlisch, Matthias},
journal={ACM SIGCOMM Computer Communication Review},
volume={48},
number={1},
pages={19--27},
year={2018},
publisher={ACM}
}
```

Github links:
* [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/rpki_collector.py)
* [emailed CSV](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/data/rov.rpki.net.json)

#### Keep your friends close, but your routeservers closer: Insights into RPKI validation in the internet

Explanation:

This paper describes a new way to obtain ROV AS information and shows a drastic increase in ROV adoption, almost 27% adoption

Paper URL: [URL](https://www.usenix.org/system/files/usenixsecurity23-hlavacek.pdf)

Paper data sources: [github](https://www.dropbox.com/s/3zr7sjkyhdrdnap/rov-2022.tar.gz?dl=0)

Bibtex:

```
@inproceedings{mixed_deployment_4,
author = {Hlavacek, Tomas and Shulman, Haya and Vogel, Niklas and Waidner, Michael},
title = {Keep Your Friends Close, but Your Routeservers Closer: Insights into RPKI Validation in the Internet},
year = {2023},
isbn = {978-1-939133-37-3},
publisher = {USENIX Association},
address = {USA},
booktitle = {Proceedings of the 32nd USENIX Conference on Security Symposium},
articleno = {271},
numpages = {18},
location = {Anaheim, CA, USA},
series = {SEC '23}
}
```

Also adding another bibtex for a poster presentation about this topic by the same authors that seems to be a subset of this work:

```
@inproceedings{mixed_deployment_5,
author = {Shulman, Haya and Vogel, Niklas and Waidner, Michael},
title = {Poster: Insights into Global Deployment of RPKI Validation},
year = {2022},
isbn = {9781450394505},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3548606.3563523},
doi = {10.1145/3548606.3563523},
booktitle = {Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security},
pages = {3467–3469},
numpages = {3},
keywords = {rpki, prefix hijacks, bgp},
location = {Los Angeles, CA, USA},
series = {CCS '22}
}
```

And adding another bibtex here that cites this work as showing 37.8% adoption. I don't think that number is correct, but it does cite it:

```
(I couldn't find the bibtex, but the paper is "The CURE to Vulnerabilities in RPKI Validation", led by Donika Mirdita, Haya Shulman, etc)
```

Github links: [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/collectors/friends_collector.py), [data](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/data/friends.json)

It's just a dropbox, and additionally, the README said that results and reproduction steps would be later published, not sure if they just forgot about this?

I am able to run the code after some extra steps, which does take a long time to run. The resulting dataset is stored in the data/friends.json file. It's important to note that this was with 8.95% network errors (I believe their paper had some of these as well) and this took place Nov 30 2023.

#### ROVISTA

Explanation:

This paper references a website with a list of ROV ASes, including an API! Super helpful

Paper URL: [Not linked, will be published IMC 2023]()

Paper data sources: [github](https://github.com/lilanleo/RoVista), [website](https://rovista.netsecurelab.org/)

Bibtex:

```
@inproceedings{mixed_deployment_6,
  author = {Weitong Li and Zhexiao Lin and Mohammad Ishtiaq Ashiq Khan and Emile Aben and Romain Fontugne and Amreesh Phokeer and Taejoong Chung},
  title = {{RoVista: Measuring and Understanding the Route Origin Validation (ROV) in RPKI}},
  booktitle = {Proceedings of the ACM Internet Measurement Conference (IMC'23)},
  address = {Montreal, Canada},
  month = {October},
  year = {2023}
}
```

Github links:
* [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/rovista_collector.py)

#### https://stats.labs.apnic.net/rpki

Explanation:

I don't think this even has a paper, it's just a website detailing ROV measurements

Paper URL: [Doesn't appear to have a paper]()

Paper data sources: [doesn't appear to have a github](), [website](https://stats.labs.apnic.net/rpki)

Bibtex:

```

@misc{mixed_deployment_7,
title={RPKI},
url={https://stats.labs.apnic.net/rpki},
author={APNIC Labs},
year={2023}
}
```

Github links:
* [Collector](https://github.com/jfuruness/rov_collector/blob/master/rov_collector/apnic_collector.py)



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
