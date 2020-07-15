# coding=utf-8
import unittest

from compiler import Parser
from io import StringIO
import itertools


class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_hasMoreCommands(self):
        buf = StringIO(u"  \n")
        parser = Parser(buf)
        self.assertFalse(parser.hasMoreCommands())
        buf = StringIO(u"//注释行\n@123")
        parser = Parser(buf)
        self.assertTrue(parser.hasMoreCommands())
        parser = Parser("test.asm")
        self.assertFalse(parser.hasMoreCommands())

    def test_advance(self):
        buf = StringIO()
        with self.assertRaisesRegexp(ValueError, "has no command.*"):
            parser = Parser(buf)
            parser.advance()
        buf = StringIO(u"@123")
        parser = Parser(buf)
        parser.advance()

    def test_commandType(self):
        buf = StringIO()
        buf.write(u"@123\n")
        buf.write(u"//\n")

        buf.write(u"(TEST_LABEL)\n")
        buf.write(u"AM=1\n")
        buf.write(u"0;JMP\n")
        buf.seek(0)
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.A_COMMAND)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.L_COMMAND)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.C_COMMAND)
        parser.advance()
        self.assertEqual(parser.commandType(), Parser.C_COMMAND)

    def test_symbol(self):
        buf = StringIO(u"(LABEL)")
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.symbol(), "LABEL")
        buf = StringIO(u"@LABEL")
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.symbol(), "LABEL")
        buf = StringIO(u"@2")
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.symbol(), "2")

    def test_dest(self):
        buf = StringIO()
        buf.write(u"M=1\n")
        buf.write(u"A;1\n")
        buf.write(u"ASD=1\n")
        buf.seek(0)
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.dest(), "M")
        with self.assertRaisesRegexp(ValueError, "Syntax error.*"):
            parser.advance()
            parser.dest()
        with self.assertRaisesRegexp(ValueError, "Syntax error.*"):
            parser.advance()
            parser.dest()

    def test_comp(self):
        buf = StringIO(u"M=A")
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.comp(), "A")

    def test_jmp(self):
        buf = StringIO(u"D;JEQ")
        parser = Parser(buf)
        parser.advance()
        self.assertEqual(parser.jmp(), "JEQ")
