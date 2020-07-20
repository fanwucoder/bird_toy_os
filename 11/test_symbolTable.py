from unittest import TestCase

from SymbolTable import SymbolTable


class TestSymbolTable(TestCase):
    def setUp(self):
        stb = SymbolTable()
        self.stb = stb
        stb.define("a", "int", "static")
        stb.define("b", "char", "field")
        stb.define("c", "bool", "arg")
        stb.define("d", "int", "var")

    def test_start_subroutine(self):
        self.stb.start_subroutine()
        self.assertEqual(self.stb.var_count("static"), 1)
        self.assertEqual(self.stb.var_count("field"), 1)
        self.assertEqual(self.stb.var_count("arg"), 0)
        self.assertEqual(self.stb.var_count("var"), 0)

    def test_define(self):
        self.stb.define("e", "int", "static")
        self.stb.define("f", "int", "field")
        self.stb.define("g", "int", "var")
        self.stb.define("h", "int", "arg")

        self.assertEqual(self.stb.var_count("static"), 2)
        self.assertEqual(self.stb.var_count("field"), 2)
        self.assertEqual(self.stb.var_count("arg"), 2)
        self.assertEqual(self.stb.var_count("var"), 2)

    def test_var_count(self):
        self.assertEqual(self.stb.var_count("static"), 1)
        self.assertEqual(self.stb.var_count("field"), 1)
        self.assertEqual(self.stb.var_count("arg"), 1)
        self.assertEqual(self.stb.var_count("var"), 1)

    def test_kind_of(self):
        self.assertEqual(self.stb.kind_of("a"), "static")
        self.assertEqual(self.stb.kind_of("b"), "field")
        self.assertEqual(self.stb.kind_of("c"), "arg")
        self.assertEqual(self.stb.kind_of("d"), "var")

    def test_type_of(self):
        self.assertEqual(self.stb.type_of("a"), "int")
        self.assertEqual(self.stb.type_of("b"), "char")
        self.assertEqual(self.stb.type_of("c"), "bool")
        self.assertEqual(self.stb.type_of("d"), "int")

    def test_index_of(self):
        self.stb.define("e", "int", "static")
        self.stb.define("f", "int", "field")
        self.stb.define("g", "int", "var")
        self.stb.define("h", "int", "arg")

        self.assertEqual(self.stb.index_of("e"), 2)
        self.assertEqual(self.stb.index_of("f"), 2)
        self.assertEqual(self.stb.index_of("g"), 2)
        self.assertEqual(self.stb.index_of("h"), 2)
