from io import StringIO
from unittest import TestCase

from Vmtranslator import Parser


class TestParser(TestCase):
    def test_hasMoreCommands(self):
        buf = StringIO(u"// \n"
                       u"push local 0\n")
        parser = Parser(buf)
        self.assertTrue(parser.hasMoreCommands())
        parser.advance()
        self.assertFalse(parser.hasMoreCommands())

    def test_advance(self):
        buf = StringIO()
        with self.assertRaisesRegexp(ValueError, "has no command.*"):
            parser = Parser(buf)
            parser.advance()
        buf = StringIO(u"push local 0")
        parser = Parser(buf)
        parser.advance()

    def test_commandType(self):
        buf = StringIO(u"""
        add
        push local 0
        pop local 0
        """)
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.C_ARITHMETIC)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.C_PUSH)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.C_POP)

    def test_arg1(self):
        buf = StringIO(u"""
               add
               push local 0
               pop argument 0
               """)
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.arg1(), "add")
        parser.advance()
        self.assertEqual(parser.arg1(), "local")
        parser.advance()
        self.assertEqual(parser.arg1(), "argument")

    def test_arg2(self):
        buf = StringIO(u"""
               add
               push local 0
               pop argument 0
               """)
        parser = Parser(buf)
        with self.assertRaisesRegexp(ValueError, ".*can not call this!"):
            parser.advance()
            parser.arg2()
        parser.advance()
        self.assertEqual(parser.arg2(), "0")

