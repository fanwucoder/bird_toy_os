from unittest import TestCase

from Vmtranslator import CodeWriter


class TestCodeWriter(TestCase):
    def test_setFileName(self):
        writer = CodeWriter("test.asm")
        with self.assertRaisesRegexp(Exception, ".*opened!"):
            writer.setFileName("test1")
        writer.close()
        writer.setFileName("test1.asm")
        writer.close()

    def test_writeArithmetic(self):
        self.fail()

    def test_writePushPop(self):
        self.fail()

    def test_close(self):
        self.fail()
