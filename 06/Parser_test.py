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
        # test_commnad = ["A", "-D", "-A", "D", "D+1", "U5", "U4", "A+1", "U6", "U1", "A-D", "U3", "U2", "D-1", "D|A",
        #                 "M+1",
        #                 "M-D", "M", "D|M", "U8", "!A", "D-A", "M+D", "!D", "!M", "D-M", "M-1", "1", "0", "-1", "-M",
        #                 "D+A", "A-1", "D&M", "D&A", "U7"]
        # buf = StringIO()
        # buf.write(u"@123\n")
        # buf.write(u"//\n")
        # cnt = 0
        # for i in itertools.combinations("AMD", 2):
        #     for x in test_commnad:
        #         dest = "".join(i)
        #         buf.write(unicode(dest + "=" + x + "\n"))
        #         cnt += 1
        # buf.write(u"//")
        # for k in ['JLT', 'JLE', 'JEQ', 'JNE', 'JGT', 'JGE']:
        #     buf.write(unicode("D;{0}\n".format(k)))
        # buf.write(u'0;JMP')
        # buf.write(u"//")
        #
        # buf.write(U"(TEST_LABEL)")
        # buf.seek(0)
        # parser = Parser(buf)
        # parser.advance()
        # self.assertEqual(parser.commandType(), Parser.A_COMMAND)
        # for i in range(cnt):
        #     parser.advance()
        #     self.assertEqual(parser.commandType(), Parser.C_COMMAND)
        # for i in range(7):
        #     parser.advance()
        #     self.assertEqual(parser.commandType(), Parser.C_COMMAND)
        # parser.advance()
        # self.assertEqual(parser.commandType(), Parser.L_COMMAND)
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
