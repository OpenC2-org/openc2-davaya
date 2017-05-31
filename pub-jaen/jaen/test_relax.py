import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load


class Relax1(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("schema", "relax1.jaen"))
        self.tc = Codec(jaen)

    def test1_property_syntax(self):
        msg_api = [{"name": "John Smith", "email": "js@example.com"},
                   {"name": "Fred Bloggs", "email": "fb@example.com", "note": "Dr."}]
        msg_min = [["John Smith", "js@example.com"],
                   ["Fred Bloggs", "fb@example.com", "Dr."]]

        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("addressBook", msg_api), msg_api)
        self.assertEqual(self.tc.decode("addressBook", msg_api), msg_api)
        self.tc.set_mode(False, False)      # Minified (list/tag)
        self.assertEqual(self.tc.encode("addressBook", msg_api), msg_min)
        self.assertEqual(self.tc.decode("addressBook", msg_min), msg_api)

class Relax2(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("schema", "relax2.jaen"))
        self.tc = Codec(jaen)

    def test1_attribute_syntax(self):
        msg_api = [{{"type": "name", "value": "John Smith"},
                    {"type": "email", "value": "js@example.com"}},
                    {"type": "name", "value": "Fred Bloggs"},
                    {"type": "email", "value": "fb@example.com"}]
        msg_min = [["John Smith", "js@example.com"],
                 ["Fred Bloggs", "fb@example.com"]]

        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("addressBook", msg_api), msg_api)
        self.assertEqual(self.tc.decode("addressBook", msg_api), msg_api)
        self.tc.set_mode(False, False)      # Minified (list/tag)
        self.assertEqual(self.tc.encode("addressBook", msg_api), msg_min)
        self.assertEqual(self.tc.decode("addressBook", msg_min), msg_api)

if __name__ == "__main__":
    unittest.main()
