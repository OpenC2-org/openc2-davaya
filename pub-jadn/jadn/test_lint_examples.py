import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_check, jadn_analyze

schema_person = {                # JADN schema for Lint Server example messages
    "meta": {"module": "LintExample1",
             "description": "Person schema from https://developers.google.com/protocol-buffers/docs/overview"},
    "types": [
        ["Person", "Record", [], "Person datatype", [
            [1, "name", "String", [], ""],
            [2, "id", "Integer", [], ""],
            [3, "email", "String", ["?"], ""],
            [4, "phone", "PhoneNumbers", ["?"], ""]
        ]],

        ["PhoneNumbers", "Array", ["#PhoneNumber"], ""],

        ["PhoneNumber", "Record", [], "", [
            [1, "number", "String", [], ""],
            [2, "type", "PhoneType", ["?"], ""]
        ]],

        ["PhoneType", "Enumerated", [], "", [
            [0, "MOBILE", ""],
            [1, "HOME", ""],
            [2, "WORK", ""]
        ]]
    ]}

class BasicTypes(unittest.TestCase):

    def setUp(self):
        jadn_check(schema_person)
        jadn_analyze(schema_person)
        self.c = Codec(schema_person, "True", "True")       # Verbose encoding mode (dict/name)

    def test_person(self):
        p1 = {
            "name": "Jon Public",
            "id": 196432}

        p2 = {
            "name": "Jon Public",
            "id": 196432,
            "email": "jon.p@example.org"}

        p3 = {
            "name": "Jon Public",
            "id": 196432,
            "phone": [
                {"number": "201-555-1234"},
                {"number": "201-555-5678", "type": "WORK"}
            ]
        }

        p4bad = {                               # Missing required id
            "name": "Jon Public"
        }

        p5bad = {                               # Bad phone type
            "name": "Jon Public",
            "id": 196432,
            "phone": [
                {"number": "201-555-1234", "type": "CELL"}
            ]
        }

        self.assertEqual(self.c.encode("Person", p1), p1)
        self.assertEqual(self.c.encode("Person", p2), p2)
        self.assertEqual(self.c.encode("Person", p3), p3)
        with self.assertRaises(ValueError):
            self.assertEqual(self.c.encode("Person", p4bad), p4bad)
        with self.assertRaises(ValueError):
            self.assertEqual(self.c.encode("Person", p5bad), p5bad)
