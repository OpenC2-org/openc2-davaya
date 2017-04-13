"""
OpenC2 Updated Examples from IACD Community Day, 23 March 2017

Use cases from "Symantec OpenC2 Proxy", Efrain Ortiz
"""

import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load
from jaen.codec.codec_utils import flatten, fluff, dlist


class OpenC2(unittest.TestCase):

    def setUp(self):
        schema = jaen_load(os.path.join("schema", "openc2.jaen"))
        self.tc = Codec(schema)

    def check(self, item, cmd_api, cmd_min, cmd_flat):
        self.tc.set_mode(False, False)      # Minified (list/tag)
        self.assertEqual(self.tc.encode(item, cmd_api), cmd_min)
        self.assertEqual(self.tc.decode(item, cmd_min), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode(item, cmd_api), cmd_api)
        self.assertEqual(self.tc.decode(item, cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)

    def test1_delete_cmd(self):
        cmd_api = {
            "action": "delete",
            "target": {
                "file": {"name": "otaku.exe",
                         "hashes": {"SHA-256": "19ce084ab0599c1659e4ce12ae822bd3"
                                               "02e494608d796b8b8a233fdfc8456663"}}},
            "actuator": {
                "endpoint_workstation": {
                    "device_id": "dns://192.168.110.120",
                    "asset_id": "B4920J"}}}

        cmd_flat = {
            "action": "delete",
            "target.file.name": "otaku.exe",
            "target.file.hashes.SHA-256": "19ce084ab0599c1659e4ce12ae822bd3"
                                          "02e494608d796b8b8a233fdfc8456663",
            "actuator.endpoint_workstation.device_id": "dns://192.168.110.120",
            "actuator.endpoint_workstation.asset_id": "B4920J"}

        cmd_min = [19,{"10":{"2":{"6":"19ce084ab0599c1659e4ce12ae822bd302e494608d796b8b8a233fdfc8456663"},
                             "4":"otaku.exe"}},{"11":["dns://192.168.110.120","B4920J"]}]

        self.check("OpenC2Command", cmd_api, cmd_min, cmd_flat)

    def test1_delete_response(self):
        cmd_api = {
            "source": "",
            "command_ref": "",
            "status": "OK",
            "statusText": "",
            "results": ""
        }
        cmd_flat = {
            "source": "",
            "command_ref": "",
            "status": "OK",
            "statusText": "",
            "results": ""
        }
        cmd_min = ["","",200,"",""]

        self.check("OpenC2Response", cmd_api, cmd_min, cmd_flat)

if __name__ == "__main__":
    unittest.main()
