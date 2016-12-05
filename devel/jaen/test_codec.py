import unittest
import codec
from jaen import jaen_check

jaen = {
    "meta": {"module": "unittests"},
    "types": [
        ["t_bool", "Boolean", [], ""],
        ["t_int", "Integer", [], ""],
        ["t_str", "String", [], ""],
        ["t_array", "Array", [], "", [
            [1, "", "Integer", [], ""]]
         ],
        ["t_attribute", "Attribute", [], "", [
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
            [2, "red", "String", [], ""],
            [4, "green", "String", [], ""],
            [6, "blue", "String", [], ""]]
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

    def test_primitive(self):
        self.assertEqual(self.test_codec.decode("t_bool", True), True)
        self.assertEqual(self.test_codec.decode("t_bool", False), False)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_bool", 1)
        self.assertEqual(self.test_codec.decode("t_int", 35), 35)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_int", True)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_int", "hello")
        self.assertEqual(self.test_codec.decode("t_str", "parrot"), "parrot")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_str", True)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_str", 1)

    def test_array(self):
        pass

    def test_attribute_min(self):
        pass

    def test_attribute_verbose(self):
        pass

    def test_choice_min(self):
        pass

    def test_choice_verbose(self):
        pass

    def test_enumerated_min(self):
        self.assertEqual(self.test_codec.decode("t_enum", 15), "extra")
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_enum", 13)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", "extra")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", ["first"])

    def test_enumerated_verbose(self):
        self.test_codec.set_mode(True, True)
        self.assertEqual(self.test_codec.decode("t_enum", "extra"), "extra")
        with self.assertRaises(ValueError):
            self.test_codec.decode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.test_codec.decode("t_enum", ["first"])

    def test_map_min(self):
        pass

    def test_map_verbose(self):
        pass

    def test_record_min(self):
        pass

    def test_record_concise(self):
        self.test_codec.set_mode(True, False)
        pass

    def test_record_verbose(self):
        self.test_codec.set_mode(True, True)
        pass

if __name__ == "__main__":
    unittest.main()
