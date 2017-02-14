import unittest
import binascii
from codec.codec import Codec
from codec.jaen import jaen_check

jaen = {                # JAEN schema for datatypes used in Basic Types tests
    "meta": {"module": "unittests-BasicTypes"},
    "types": [
        ["t_bool", "Boolean", [], ""],
        ["t_int", "Integer", [], ""],
        ["t_num", "Number", [], ""],
        ["t_str", "String", [], ""],
        ["t_bin", "Binary", [], ""],
        ["t_array", "Array", [], "", [
            [0, "", "Integer", [], ""]]
         ],
        ["t_choice", "Choice", [], "", [
            [1, "type1", "String", [], ""],
            [4, "type2", "Boolean", [], ""],
            [7, "type3", "Integer", [], ""]]
         ],
        ["t_enum", "Enumerated", [], "", [
            [1, "first", ""],
            [15, "extra", ""],
            [8, "Chunk", ""]]
         ],
        ["t_map", "Map", [], "", [
            [2, "red", "Integer", [], ""],
            [4, "green", "Integer", ["?"], ""],
            [6, "blue", "Integer", [], ""],
            [9, "alpha", "Integer", ["?"], ""]]
         ],
        ["t_rec", "Record", [], "", [
            [1, "red", "Integer", [], ""],
            [2, "green", "Integer", ["?"], ""],
            [3, "blue", "Integer", [], ""],
            [4, "alpha", "Integer", ["?"], ""]]
         ]
    ]}


class BasicTypes(unittest.TestCase):

    def setUp(self):
        jaen_check(jaen)
        self.tc = Codec(jaen)

    def test_primitive(self):   # Non-composed types (bool, int, num, str)
        self.assertEqual(self.tc.decode("t_bool", True), True)
        self.assertEqual(self.tc.decode("t_bool", False), False)
        self.assertEqual(self.tc.encode("t_bool", True), True)
        self.assertEqual(self.tc.encode("t_bool", False), False)
        with self.assertRaises(TypeError):
            self.tc.decode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.tc.decode("t_bool", 1)
        with self.assertRaises(TypeError):
            self.tc.encode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.tc.encode("t_bool", 1)

        self.assertEqual(self.tc.decode("t_int", 35), 35)
        self.assertEqual(self.tc.encode("t_int", 35), 35)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", "hello")
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", "hello")

        self.assertEqual(self.tc.decode("t_num", 25.96), 25.96)
        self.assertEqual(self.tc.decode("t_num", 25), 25)
        self.assertEqual(self.tc.encode("t_num", 25.96), 25.96)
        self.assertEqual(self.tc.encode("t_num", 25), 25)
        with self.assertRaises(TypeError):
            self.tc.decode("t_num", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_num", "hello")
        with self.assertRaises(TypeError):
            self.tc.encode("t_num", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_num", "hello")

        self.assertEqual(self.tc.decode("t_str", "parrot"), "parrot")
        self.assertEqual(self.tc.encode("t_str", "parrot"), "parrot")
        with self.assertRaises(TypeError):
            self.tc.decode("t_str", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_str", 1)
        with self.assertRaises(TypeError):
            self.tc.encode("t_str", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_str", 1)

    def test_array(self):
        self.assertEqual(self.tc.decode("t_array", [1, 4, 9, 16]), [1, 4, 9, 16])
        self.assertEqual(self.tc.encode("t_array", [1, 4, 9, 16]), [1, 4, 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array", 9)
        with self.assertRaises(TypeError):
            self.tc.encode("t_array", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array", 9)

    B1b = b"data to be encoded"
    B1s = "ZGF0YSB0byBiZSBlbmNvZGVk"
    B2b = "data\nto be ëncoded 旅程".encode(encoding="UTF-8")
    B2s = "ZGF0YQp0byBiZSDDq25jb2RlZCDml4XnqIs="
    B3b = binascii.a2b_hex("18e0c9987b8f32417ca6744f544b815ad2a6b4adca69d2c310bd033c57d363e3")
    B3s = "GODJmHuPMkF8pnRPVEuBWtKmtK3KadLDEL0DPFfTY+M="

    def test_binary(self):
        self.assertEqual(self.tc.decode("t_bin", self.B1s), self.B1b)
        self.assertEqual(self.tc.decode("t_bin", self.B2s), self.B2b)
        self.assertEqual(self.tc.decode("t_bin", self.B3s), self.B3b)
        self.assertEqual(self.tc.encode("t_bin", self.B1b), self.B1s)
        self.assertEqual(self.tc.encode("t_bin", self.B2b), self.B2s)
        self.assertEqual(self.tc.encode("t_bin", self.B3b), self.B3s)

    C1a = {"type1": "foo"}
    C2a = {"type2": False}
    C3a = {"type3": 42}
    C1m = {1: "foo"}
    C2m = {4: False}
    C3m = {7: 42}
    C1_bad1a = {"type1": 15}
    C1_bad2a = {"type4": "foo"}
    C1_bad3a = {"type1": "foo", "type2": False}
    C1_bad1m = {1: 15}
    C1_bad2m = {3: "foo"}
    C1_bad3m = {1: "foo", 4: False}

    def test_choice_min(self):
        self.assertEqual(self.tc.decode("t_choice", self.C1m), self.C1a)
        self.assertEqual(self.tc.decode("t_choice", self.C2m), self.C2a)
        self.assertEqual(self.tc.decode("t_choice", self.C3m), self.C3a)
        self.assertEqual(self.tc.encode("t_choice", self.C1a), self.C1m)
        self.assertEqual(self.tc.encode("t_choice", self.C2a), self.C2m)
        self.assertEqual(self.tc.encode("t_choice", self.C3a), self.C3m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_choice", self.C1_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad2m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad3m)
        with self.assertRaises(TypeError):
            self.tc.encode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad3a)


    def test_choice_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_choice", self.C1a), self.C1a)
        self.assertEqual(self.tc.decode("t_choice", self.C2a), self.C2a)
        self.assertEqual(self.tc.decode("t_choice", self.C3a), self.C3a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad3a)


    def test_enumerated_min(self):
        self.assertEqual(self.tc.decode("t_enum", 15), "extra")
        self.assertEqual(self.tc.encode("t_enum", "extra"), 15)
        with self.assertRaises(ValueError):
            self.tc.decode("t_enum", 13)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", "extra")
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.tc.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", 15)
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", [1])

    def test_enumerated_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_enum", "extra"), "extra")
        self.assertEqual(self.tc.encode("t_enum", "extra"), "extra")
        with self.assertRaises(ValueError):
            self.tc.decode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.tc.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", ["first"])

    RGB1 = {"red": 24, "green": 120, "blue": 240}    # API (decoded) values
    RGB2 = {"red": 50, "blue": 100}
    RGBA = {"red": 9, "green": 80, "blue": 96, "alpha": 128}
    RGB1_bad1a = {"red": 24, "green": 120}
    RGBA_bad2a = {"red": 9, "green": 80, "blue": 96, "alpha": 128, "beta": 196}
    RGB1_bad3a = {"red": "four", "green": 120, "blue": 240}
    RGB1_bad4a = {2: 24, "green": 120, "blue": 240}

    RGB1m = {2: 24, 4: 120, 6: 240}                  # Encoded values (minimized)
    RGB2m = {2: 50, 6: 100}
    RGBAm = {2: 9, 4: 80, 6: 96, 9: 128}
    RGB1_bad1m = {2: 24, 4: 120}
    RGBA_bad2m = {2: 9, 4: 80, 6: 96, 9: 128, 12: 42}
    RGB1_bad3m = {2: "four", 4: 120, 6: 240}
    RGB1_bad4m = {"2": 24, 4: 120, 6: 240}

    RGB1c = [24, 120, 240]                           # Encoded values (concise)
    RGB2c = [50, None, 100]
    RGBAc = [9, 80, 96, 128]
    RGB1_bad1c = [24, 120]
    RGBA_bad2c = [9, 80, 96, 128, 42]
    RGB1_bad3c = ["four", 120, 240]

    RGB1_bad1v = {"red": 24, "green": "120", "blue": 240}    # Encoded values (verbose)
    RGB1_bad2v = {"red": 24, "green": 120, "bleu": 240}
    RGB1_bad3v = {2: 24, "green": 120, "blue": 240}
    RGBA_bad4v = {"red": 9, "green": 80, "blue": 96, "beta": 128}

    def test_map_min(self):
        self.assertDictEqual(self.tc.decode("t_map", self.RGB1m), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB2m), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_map", self.RGBAm), self.RGBA)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.RGB1m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB2), self.RGB2m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGBA), self.RGBAm)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB1_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGBA_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB1_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB1_bad4m)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB1_bad3a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB1_bad4a)

    def test_map_verbose(self):     # Encoding identical to record_verbose
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.RGBA), self.RGBA)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode("t_map", self.RGBA), self.RGBA)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB1_bad1v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB1_bad2v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB1_bad3v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGBA_bad4v)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB1_bad3a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB1_bad4a)

    def test_record_concise(self):
        self.tc.set_mode(False, True)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB1c), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB2c), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGBAc), self.RGBA)
        self.assertEqual(self.tc.encode("t_rec", self.RGB1), self.RGB1c)
        self.assertEqual(self.tc.encode("t_rec", self.RGB2), self.RGB2c)
        self.assertEqual(self.tc.encode("t_rec", self.RGBA), self.RGBAc)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB1_bad1c)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGBA_bad2c)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.RGB1_bad3c)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB1_bad3a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB1_bad4a)

    def test_record_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGBA), self.RGBA)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGBA), self.RGBA)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.RGB1_bad1v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB1_bad2v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB1_bad3v)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGBA_bad4v)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB1_bad3a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB1_bad4a)

if __name__ == "__main__":
    unittest.main()
