from unittest import TestCase

from JackTokenizer import JackTokenizer, TokenType, KeywordType
from io import StringIO


class TestJackTokenizer(TestCase):

    def test_has_more_tokens(self):
        buf = StringIO("""
        /*空文件，没有内容
        */
        /*空文件，当行注释移除*/
        """)
        tokenizer = JackTokenizer(buf)
        self.assertFalse(tokenizer.has_more_tokens())
        buf = StringIO("""
        class Main{  /*空文件，没有内容
        */        }
        """)
        tokenizer = JackTokenizer(buf)
        self.assertTrue(tokenizer.has_more_tokens())

    def test_advance(self):
        buf = StringIO("""
        /*空文件，没有内容
        */
        """)
        tokenizer = JackTokenizer(buf)
        with self.assertRaisesRegex(ValueError, "has no more tokens.*"):
            tokenizer.advance()
        buf = StringIO("""
        class Main{
        }
        """)
        tokenizer = JackTokenizer(buf)
        tokenizer.advance()

    def test_token_type(self):
        tokenizer = JackTokenizer("ArrayTest/Main.jack")
        tokenizer.advance()
        self.assertEqual(TokenType.KEY_WORD, tokenizer.token_type())
        self.assertEqual(tokenizer.keyword(), KeywordType.CLASS)
        tokenizer.advance()
        self.assertEqual(TokenType.IDENTIFIER, tokenizer.token_type())
        self.assertEqual(tokenizer.identifier(), "Main")

        tokenizer.advance()
        self.assertEqual(TokenType.SYMBOL, tokenizer.token_type())
        self.assertEqual(tokenizer.symbol(), "{")

        i = 0
        while tokenizer.has_more_tokens():
            i += 1
            tokenizer.advance()
            if i == 43:
                self.assertEqual(TokenType.INT_CONSTANT, tokenizer.token_type())
                self.assertEqual(tokenizer.intVal(), 0)
            if i == 28:
                self.assertEqual(TokenType.STRING_CONSTANT, tokenizer.token_type())
                self.assertEqual(tokenizer.stringVal(), "HOW MANY NUMBERS? ")
