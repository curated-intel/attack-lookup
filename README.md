# MITRE ATT&CK Lookup Tool

[![PyPi license](https://badgen.net/pypi/license/attack-lookup/)](https://pypi.org/project/attack-lookup/) [![PyPi version](https://badgen.net/pypi/v/attack-lookup/)](https://pypi.org/project/attack-lookup/)

`attack-lookup` is a tool that lets you easily check what Tactic, Technique, or Sub-technique ID maps to what name, and vice versa. It can be used interactively, for batch processing, or in your own tooling. 

## Installation

`attack-lookup` can be installed from PyPi:

```
$ pip install attack-lookup
```

It can also be installed manually:

```
$ git clone https://github.com/curated-intel/attack-lookup.git
$ cd attack-lookup
$ python setup.py install --user
```

## Usage

```
$ attack-lookup --help
usage: attack-lookup [-h] [-v VERSION] [-m {enterprise,ics,mobile}] [-O] [-i INPUT] [-o OUTPUT] [--output-mode {results,csv}]

MITRE ATT&CK Lookup Tool

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        ATT&CK matrix version to use (default: v10.1)
  -m {enterprise,ics,mobile}, --matrix {enterprise,ics,mobile}
                        ATT&CK matrix to use (default: enterprise)
  -O, --offline         Run in offline mode (default: False)
  -i INPUT, --input INPUT
                        Path to input file (one lookup value per line) (default: None)
  -o OUTPUT, --output OUTPUT
                        Path to output file (default: -)
  --output-mode {results,csv}
                        Mode for output file ("result" only has the lookup results, "csv" outputs a CSV with the lookup and result values (default: results)
```

By default, `attack-lookup` uses the latest version of the Enterprise matrix. When running in Online mode, `attack-lookup` pulls the latest matrix from MITRE's GitHub [repo](https://github.com/mitre/cti). When running in Offline mode, it can use any matrix available in `attack_lookup/data`.

You can use `attack-lookup` in interactive or batch mode:

```
$ attack-lookup
(loading latest enterprise matrix...done)
Running attack-lookup in interactive mode, exit with (q)uit
ATT&CK> T1539
Steal Web Session Cookie
ATT&CK>
```

For batch mode, specify an input file, and optionally an output file/mode. By default, output will go to `stdout`.
```
$ attack-lookup -i test
(loading latest enterprise matrix...done)
Collection
T1133
Peripheral Device Discovery

$ attack-lookup -i test --output-mode=csv
(loading latest enterprise matrix...done)
TA0009,Collection
External Remote Services,T1133
T1120,Peripheral Device Discovery

$ attack-lookup -i test --output-mode=csv -o out_file
(loading latest enterprise matrix...done)
Wrote output data to out_file
```

If multiple mappings exist (e.g., "Domains"), `attack-lookup` will provide all possible values:
```
ATT&CK> Domains
Multiple possible values: T1583.001, T1584.001
```

## API

You can also use `attack-lookup` in your own scripts.

```py
from attack_lookup import AttackMapping

# version is ignored when running online FYSA
mapping = AttackMapping(matrix="enterprise", version="v10.1", offline=False)

# load the data
# this can take ~10sec
if not mapping.load_data():
    print("failed to load data")
else:
    mapping.lookup("T1574") # returns "Hijack Execution Flow"
```
