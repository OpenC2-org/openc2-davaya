import json
import os
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load
from libs.codec.codec_utils import flatten, fluff, dlist


class OpenC2(unittest.TestCase):

    def setUp(self):
        schema = jadn_load(os.path.join("schema", "openc2.jadn"))
        self.tc = Codec(schema, True, True)

    def test01_high_level(self):
        cmd_api = {
            "action": "deny",
            "target": {
                "ip_connection": {
                    "src_addr":"1.2.3.4",
                    "src_port": 21,
                    "layer4_protocol": "tcp"
                }}}

        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        print(json.dumps(cmd_api, indent=2))

