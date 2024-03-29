"""
OpenC2 Updated Examples from IACD Community Day, 23 March 2017

Use cases from "Symantec OpenC2 Proxy", Efrain Ortiz
"""

import os
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load
from libs.codec.codec_utils import flatten, fluff, dlist

0
class OpenC2(unittest.TestCase):

    def setUp(self):
        schema = jadn_load(os.path.join("schema", "openc2.jadn"))
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
                    "actuator_id": "dns://192.168.110.120",
                    "asset_id": "B4920J"}},
            "modifiers": {
                "command_id": "SEP1432_84295"
            }
        }

        cmd_flat = {
            "action": "delete",
            "target.file.name": "otaku.exe",
            "target.file.hashes.SHA-256": "19ce084ab0599c1659e4ce12ae822bd3"
                                          "02e494608d796b8b8a233fdfc8456663",
            "actuator.endpoint_workstation.actuator_id": "dns://192.168.110.120",
            "actuator.endpoint_workstation.asset_id": "B4920J",
            "modifiers.command_id": "SEP1432_84295"}

        cmd_min = [19,{"10":{"2":{"6":"19ce084ab0599c1659e4ce12ae822bd302e494608d796b8b8a233fdfc8456663"},
                  "4":"otaku.exe"}},{"11":["dns://192.168.110.120","B4920J"]},{"6":"SEP1432_84295"}]

        self.check("OpenC2Command", cmd_api, cmd_min, cmd_flat)

    def test1_delete_response(self):
        cmd_api = {
            "status": "OK",
            "response_src": "dns://192.168.110.120"
        }
        cmd_flat = cmd_api
        cmd_min = [200,None,"dns://192.168.110.120"]

        self.check("OpenC2Response", cmd_api, cmd_min, cmd_flat)

    def test2_respond_cmd(self):
        cmd_api = {
            "action": "report",
            "target": {"url":"dummy"},
            "actuator": {
                "endpoint_workstation": {
                    "actuator_id": "dns://192.168.110.120"}},
            "modifiers": {
                "respond_to": "dns://remote-server14.example.com",
                "command_ref": "SEP1432_84295"
            }
        }

        cmd_flat = {
            "action": "report",
            "target.url": "dummy",
            "actuator.endpoint_workstation.actuator_id": "dns://192.168.110.120",
            "modifiers.respond_to": "dns://remote-server14.example.com",
            "modifiers.command_ref": "SEP1432_84295"
        }

        cmd_min = [4,{"18":"dummy"},{"11":["dns://192.168.110.120"]},{"9":"dns://remote-server14.example.com","17":"SEP1432_84295"}]

        self.check("OpenC2Command", cmd_api, cmd_min, cmd_flat)

if __name__ == "__main__":
    unittest.main()
