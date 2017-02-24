import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load


class OpenC2(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("data", "openc2.jaen"))
        self.tc = Codec(jaen)

    def test_query(self):
        cmd2_api1 = {           # Literal STIX Object
            "action": "scan",
            "target": {
                "0": {
                    "type": "domain-name",
                    "value": "www.example.com",
                    "resolves_to_refs": ["1", "2"]
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "198.51.100.2"
                },
                "2": {
                    "type": "domain-name",
                    "value": "ms34.example.com"
                }
            }
        }

        cmd2_api2 = {           # Type-Specifiers
            "action": "scan",
            "target": {
                "type": "domain-name",
                "specifiers": {
                    "value": "www.example.com",
                    "resolves_to": [{
                        "type": "ipv4-addr",
                        "value": "198.51.100.2"
                    },{
                        "type": "domain-name",
                        "value": "ms34.example.com"
                    }]
                }
            }
        }

        cmd2_api3 = {           # Type as property name
            "action": "scan",
            "target": {
                "domain-name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"v4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}
                    ]
                }
            }
        }

        cmd2_min3 = [1,{"7":["www.example.com",[{"1":["198.51.100.2"]},{"3":["ms34.example.com"]}]]}]

        t_api3 = self.tc.decode("OpenC2Command", cmd2_min3)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_min3), cmd2_api3)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api3), cmd2_min3)

        cmd1_api = {"action": "query", "target": {"commands":{}}}
        cmd1_flat = {"action": "query", "target.commands":{}}
        cmd1_concise = ["query", ["commands"]]
        cmd1_noname = {"1":3, "2":{"1":2}}
        cmd1_min = [3,{"2":""}]
                                        # Minified (list/tag)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_min), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_min)
        self.tc.set_mode(True, False)   # not named, but check dict/tag mode anyway
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_noname), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_noname)
        self.tc.set_mode(False, True)   # Concise (list/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_concise), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_concise)
        self.tc.set_mode(True, True)    # Verbose (dict/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_api), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_api)

if __name__ == "__main__":
    unittest.main()
