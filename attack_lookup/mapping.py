import json
import os
import re
import sys
from typing import Dict, Union

import requests
from stix2 import MemoryStore
from stix2.datastore.filters import Filter

class AttackMapping:
    valid_matrices = ["enterprise", "ics", "mobile"]

    def __init__(self, matrix: str = "enterprise", version: str = "v10.1", offline: bool = False):
        if matrix not in AttackMapping.valid_matrices:
            raise ValueError(f"Invalid matrix specified. Valid matrices are: [{', '.join(AttackMapping.valid_matrices)}]")

        self.matrix = matrix

        if version[0] != "v":
            version = "v" + version
        self.version = version

        self.offline = offline

        # ID -> Name
        self.mapping: Dict[str, str] = {}

        self.stix_store: MemoryStore = None

    def _get_json_for_matrix(self) -> Union[Dict, None]:
        if self.offline:
            dirname = os.path.dirname(__file__)
            # check if the requested version is available
            if not os.path.exists(f"{dirname}/data/{self.version}"):
                print(f"Offline data not available for {self.version}, please run with online mode")
                return None
            
            # check if the matrix for the version is available
            if not os.path.exists(f"{dirname}/data/{self.version}/{self.matrix}-attack.json"):
                print(f"Offline data not available for {self.matrix} {self.version}, please run with online mode")
                return None

            # data exists for version + matrix, load it in
            with open(f"{dirname}/data/{self.version}/{self.matrix}-attack.json", "r") as f:
                return json.loads(f.read())
        else:
            # online mode, download the latest version
            url = f"https://raw.githubusercontent.com/mitre/cti/master/{self.matrix}-attack/{self.matrix}-attack.json"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                print(f"Failed to download ATT&CK data from GitHub, status code was {r.status_code}")
                return None
            
            # got the data
            return r.json()

    def load_data(self) -> bool:
        sys.stderr.write(f"(loading {'latest' if not self.offline else 'offline'} {self.matrix} {self.version + ' ' if self.offline else ''}matrix...")
        sys.stderr.flush()

        json_data = self._get_json_for_matrix()
        if json_data is None:
            return False

        # load into STIX MS
        stix_ms = MemoryStore(stix_data=json_data["objects"])
        self.stix_store = stix_ms

        # build mapping dict
        # ref: https://github.com/mitre-attack/mitreattack-python/blob/master/mitreattack/attackToExcel/stixToDf.py
        techniques = stix_ms.query(Filter("type", "=", "attack-pattern"))
        tactics = stix_ms.query(Filter("type", "=", "x-mitre-tactic"))
        items = []
        items.extend(techniques)
        items.extend(tactics)
        for t in items:
            name = t["name"]

            sources = ("mitre-attack", "mitre-ics-attack", "mitre-mobile-attack")

            id = list(filter(lambda x: x["source_name"] in sources, t["external_references"]))[0]["external_id"]

            self.mapping[id] = name
        
        sys.stderr.write("done)" + os.linesep)
        sys.stderr.flush()

        return True
    
    def lookup(self, src_val: str) -> Union[str, None]:
        if len(self.mapping.keys()) == 0:
            print("Mapping is empty, did you call AttackMapping.load_data()?")
            return None

        src_val = src_val.strip()

        val = ""

        # check if the src val we have is an ID
        # they can be TA####, T####, or T####.###
        id_re = re.compile(r"^TA?[0-9]{4}(\.[0-9]{3})?$", re.IGNORECASE)
        if id_re.match(src_val):
            # we have an ID, get the value from the map
            try:
                val = [value for key, value in self.mapping.items() if key.lower() == src_val.lower()]
            except KeyError:
                pass
        else:
            # we have a name, get the ID
            # https://www.kite.com/python/answers/how-to-do-a-reverse-dictionary-lookup-in-python
            lookup_dict = [key for key, value in self.mapping.items() if value.lower() == src_val.lower()]
            if len(lookup_dict) == 1:
                val = lookup_dict[0]
            elif len(lookup_dict) > 1:
                # some values have multiple, such as the subtechniques in resource development
                val = "Multiple possible values: " + ", ".join(lookup_dict)
        
        if len(val) == 0:
            val = f"<No value found for \"{src_val}\">"
        
        return val