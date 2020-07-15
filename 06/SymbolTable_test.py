# coding=utf-8
import unittest
from compiler import SymbolTable


class TestSymbolTable(unittest.TestCase):
    def setUp(self):
        self.st = SymbolTable()
        self.st.addEntry("test1", 1)
        self.st.addEntry("has_key", 2)

    def test_addEntry(self):
        self.st.addEntry("addkey", 2)
        self.assertTrue(self.st.contains("addkey"))

    def test_contains(self):
        self.assertTrue(self.st.contains("has_key"))

    def test_getAddress(self):
        self.assertEqual(1, self.st.getAddress("test1"))


if __name__ == '__main__':
    unittest.main()
