import unittest
import codec
from jaen import jaen_check

jaen = {
    "meta": {"module": "unittests-BasicTypes"},
    "types": [
        ["t_bool", "Boolean", [], ""],
        ["t_int", "Integer", [], ""],
        ["t_num", "Number", [], ""],
        ["t_str", "String", [], ""],
        ["t_array", "Array", [], "", [
            [0, "", "Integer", [], ""]]
         ],
        ["t_attr", "Attribute", [], "", [
            [3, "alpha", "String", [], ""],
            [5, "beta", "Integer", [], ""]]
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
            [4, "green", "Integer", [], ""],
            [6, "blue", "Integer", [], ""],
            [9, "alpha", "Integer", ["?"], ""]]
         ],
        ["t_rec", "Record", [], "", [
            [1, "red", "Integer", [], ""],
            [2, "green", "Integer", [], ""],
            [3, "blue", "Integer", [], ""],
            [4, "alpha", "Integer", ["?"], ""]]
         ]
    ]}


class BasicTypes(unittest.TestCase):

    def setUp(self):
        jaen_check(jaen)
        self.test_codec = codec.Codec(jaen)

    def test_primitive(self):   # Non-composed types (bool, int, num, str)
        self.assertEqual(self.test_codec.decode("t_bool", True), True)
        self.assertEqual(self.test_codec.decode("t_bool", False), False)
        self.assertEqual(self.test_codec.encode("t_bool", True), True)
        self.assertEqual(self.test_codec.encode("t_bool", False), False)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_bool", 1)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_bool", 1)

        self.assertEqual(self.test_codec.decode("t_int", 35), 35)
        self.assertEqual(self.test_codec.encode("t_int", 35), 35)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_int", True)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_int", "hello")
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_int", True)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_int", "hello")

        self.assertEqual(self.test_codec.decode("t_num", 25.96), 25.96)
        self.assertEqual(self.test_codec.decode("t_num", 25), 25)
        self.assertEqual(self.test_codec.encode("t_num", 25.96), 25.96)
        self.assertEqual(self.test_codec.encode("t_num", 25), 25)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_num", True)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_num", "hello")
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_num", True)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_num", "hello")

        self.assertEqual(self.test_codec.decode("t_str", "parrot"), "parrot")
        self.assertEqual(self.test_codec.encode("t_str", "parrot"), "parrot")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_str", True)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_str", 1)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_str", True)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_str", 1)

    def test_array(self):
        self.assertEqual(self.test_codec.decode("t_array", [1, 4, 9, 16]), [1, 4, 9, 16])
        self.assertEqual(self.test_codec.encode("t_array", [1, 4, 9, 16]), [1, 4, 9, 16])
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_array", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_array", 9)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_array", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_array", 9)

    def test_attribute_min(self):
        pass

    def test_attribute_verbose(self):
        self.test_codec.set_mode(True, True)
        pass

    def test_choice_min(self):
        pass

    def test_choice_verbose(self):
        self.test_codec.set_mode(True, True)
        pass

    def test_enumerated_min(self):
        self.assertEqual(self.test_codec.decode("t_enum", 15), "extra")
        self.assertEqual(self.test_codec.encode("t_enum", "extra"), 15)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_enum", 13)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", "extra")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_enum", 15)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_enum", [1])

    def test_enumerated_verbose(self):
        self.test_codec.set_mode(True, True)
        self.assertEqual(self.test_codec.decode("t_enum", "extra"), "extra")
        self.assertEqual(self.test_codec.encode("t_enum", "extra"), "extra")
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_enum", ["first"])

    RGB = {"red": 24, "green": 120, "blue": 240}    # API (decoded) values
    RGBA = {"red": 9, "green": 80, "blue": 96, "alpha": 128}
    RGB_bad1a = {"red": 24, "green": 120}
    RGBA_bad2a = {"red": 9, "green": 80, "blue": 96, "alpha": 128, "beta": 196}
    RGB_bad3a = {"red": "four", "green": 120, "blue": 240}
    RGB_bad4a = {2: 24, "green": 120, "blue": 240}

    RGBm = {2: 24, 4: 120, 6: 240}                  # Encoded values (minimized)
    RGBAm = {2: 9, 4: 80, 6: 96, 9: 128}
    RGB_bad1m = {2: 24, 4: 120}
    RGBA_bad2m = {2: 9, 4: 80, 6: 96, 9: 128, 12: 42}
    RGB_bad3m = {2: "four", 4: 120, 6: 240}
    RGB_bad4m = {"2": 24, 4: 120, 6: 240}
    RGB_bad1v = {"red": 24, "green": "120", "blue": 240}
    RGB_bad2v = {"red": 24, "green": 120, "bleu": 240}
    RGBA_bad3v = {"red": 9, "green": 80, "blue": 96, "beta": 128}
    RGB_bad4v = {2: 24, "green": 120, "blue": 240}

    def test_map_min(self):
        self.test_codec.set_mode(False, False)
        self.assertDictEqual(self.test_codec.decode("t_map", self.RGBm), self.RGB)
        self.assertDictEqual(self.test_codec.decode("t_map", self.RGBAm), self.RGBA)
        self.assertDictEqual(self.test_codec.encode("t_map", self.RGB), self.RGBm)
        self.assertDictEqual(self.test_codec.encode("t_map", self.RGBA), self.RGBAm)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_map", self.RGB_bad1m)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_map", self.RGBA_bad2m)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_map", self.RGB_bad3m)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_map", self.RGB_bad4m)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_map", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_map", self.RGB_bad4a)

    def test_map_verbose(self):     # Encoding identical to record_verbose
        self.test_codec.set_mode(True, True)
        self.assertDictEqual(self.test_codec.decode("t_map", self.RGB), self.RGB)
        self.assertDictEqual(self.test_codec.decode("t_map", self.RGBA), self.RGBA)
        self.assertDictEqual(self.test_codec.encode("t_map", self.RGB), self.RGB)
        self.assertDictEqual(self.test_codec.encode("t_map", self.RGBA), self.RGBA)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_map", self.RGB_bad1v)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_map", self.RGB_bad2v)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_map", self.RGBA_bad3v)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_map", self.RGB_bad4v)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_map", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_map", self.RGB_bad4a)

    RGBc = [24, 120, 240]                           # Encoded values (concise)
    RGBAc = [9, 80, 96, 128]
    RGB_bad1c = [24, 120]
    RGBA_bad2c = [9, 80, 96, 128, 42]
    RGB_bad3c = ["four", 120, 240]

    def test_record_concise(self):
        self.test_codec.set_mode(True, False)
        self.assertDictEqual(self.test_codec.decode("t_rec", self.RGBc), self.RGB)
        self.assertDictEqual(self.test_codec.decode("t_rec", self.RGBAc), self.RGBA)
        self.assertDictEqual(self.test_codec.encode("t_rec", self.RGB), self.RGBc)
        self.assertDictEqual(self.test_codec.encode("t_rec", self.RGBA), self.RGBAc)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_rec", self.RGB_bad1c)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_rec", self.RGBA_bad2c)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_rec", self.RGB_bad3c)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_rec", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_rec", self.RGB_bad4a)

    def test_record_verbose(self):
        self.test_codec.set_mode(True, True)
        self.assertDictEqual(self.test_codec.decode("t_rec", self.RGB), self.RGB)
        self.assertDictEqual(self.test_codec.decode("t_rec", self.RGBA), self.RGBA)
        self.assertDictEqual(self.test_codec.encode("t_rec", self.RGB), self.RGB)
        self.assertDictEqual(self.test_codec.encode("t_rec", self.RGBA), self.RGBA)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_rec", self.RGB_bad1v)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_rec", self.RGB_bad2v)
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_rec", self.RGBA_bad3v)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_rec", self.RGB_bad4v)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.test_codec.encode("t_rec", self.RGBA_bad2a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.test_codec.encode("t_rec", self.RGB_bad4a)

if __name__ == "__main__":
    unittest.main()
