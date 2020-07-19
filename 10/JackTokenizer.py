# coding=utf-8
import os
import re
from enum import Enum
from io import IOBase, StringIO
import sys
from typing import Optional

KEY_WORDS = ['class', 'constructor', 'function',
             'method', 'field',
             'static', 'var',
             'int', 'char', 'boolean',
             'void', 'true', 'false', "null", 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbol = list("[]{}().,;+-*/&|<>=~")
check_re = re.compile("|".join(["(k )".format(k) for k in KEY_WORDS]))
if sys.version_info.major == 3:
    unicode = str
    from io import TextIOWrapper

    file = TextIOWrapper


class TokenType(Enum):
    stringConstant = 4
    intConstant = 3
    identifier = 2
    keyword = 0
    symbol = 1


class KeywordType(Enum):
    CLASS = 0
    CONSTRUCTOR = 1
    FUNCTION = 2
    METHOD = 3
    FIELD = 4
    STATIC = 5
    VAR = 6
    INT = 7
    CHAR = 8
    BOOLEAN = 9
    VOID = 10
    TRUE = 11
    FALSE = 12
    NULL = 13
    THIS = 14
    LET = 15
    DO = 16
    IF = 17
    ELSE = 18
    WHILE = 19
    RETURN = 20


class JackTokenizer(object):

    def __init__(self, filename):

        self._key_word = None
        self._file = filename
        self._buf = None
        self.line = 0
        self._all_lines = []
        self._token = None
        self._token_type = None
        self.command = None  # type: Optional[str]
        self._tokens = []  # type: Optional[list[str]]
        self._init_()

    def _init_(self):
        if isinstance(self._file, str) or isinstance(self._file, unicode):
            self._buf = open(self._file, 'r')
        elif isinstance(self._file, file) or isinstance(self._file, IOBase):
            self._buf = self._file
        else:
            raise ValueError("file object show file or readable")
        self._remove_comment()

    def _remove_comment(self):
        is_block_comment = False
        i = 0
        for line in self._buf.readlines():  # type: str
            line = line.strip()
            i += 1
            if line.strip() == '':
                continue
            if is_block_comment:
                b = line.find("*/")
                if b != -1:
                    line = line[b + 2:]
                    is_block_comment = False

            if "/*" in line:
                while line.find("/*") != -1:
                    a = line.find("/*")
                    b = line.find("*/")
                    if b != -1:
                        # 单行的/**/类型注释
                        line = line.replace(line[a:b + 2], "")
                    else:
                        line = line[:a]
                        is_block_comment = True
                if line.strip():
                    self._all_lines.append((i, line))
                continue
            if line.startswith("//"):
                continue
            line = line.split("//")[0]
            if line.strip():
                self._all_lines.append((i, line.strip()))
        print(self._all_lines)
        self._buf.close()

    def has_more_tokens(self):
        return len(self._all_lines) != 0 or len(self._tokens) != 0

    def advance(self):
        if not self.has_more_tokens():
            raise ValueError("has no more tokens")
        # 当前行已经分析完了
        if len(self._tokens) == 0:
            self.line, self.command = self._all_lines[0]
            self._split_tokens()
            self._all_lines.pop(0)

        self._token = self._tokens[0]
        self._tokens.pop(0)
        if self._iskeyword(self._token):
            self._token_type = TokenType.keyword
            self._key_word = KeywordType(KEY_WORDS.index(self._token))
        elif self._is_symbol(self._token):
            self._token_type = TokenType.symbol
        elif self._is_int_constant(self._token):
            self._token_type = TokenType.intConstant
        elif self._is_string_constant(self._token):
            self._token_type = TokenType.stringConstant
        elif self._is_identifier(self._token):
            self._token_type = TokenType.identifier
        else:
            raise ValueError("unknown token type:%s,%s" % (self.line, self._token))

    def token_type(self):
        # print(self._token, self._token_type)
        return self._token_type

    def keyword(self):
        return self._key_word

    def symbol(self):
        return self._token

    def identifier(self):
        return self._token

    def intVal(self):
        return self._token

    def stringVal(self):
        return self._token[1:-1]

    def _iskeyword(self, token):
        return token in KEY_WORDS

    def _is_symbol(self, token):
        return token in symbol

    def _is_identifier(self, _token):
        return re.match("[a-zA-Z_][a-zA-Z0-9]*", _token)

    def _is_int_constant(self, token):
        return re.match("[0-9]+", token) is not None

    def _is_string_constant(self, token):
        return re.match('"[^"]*"', token)

    def _split_tokens(self):
        cmd = self.command
        self._tokens = []
        while cmd.find('\"') != -1:
            a = cmd.find('\"')
            b = cmd.find("\"", a + 1)
            self._tokens = self._tokens + self._split_by_symbol(cmd[:a])
            self._tokens.append(cmd[a:b + 1])
            cmd = cmd[b:]
        self._tokens = self._tokens + self._split_by_symbol(cmd)
        self._tokens = [x for x in self._tokens if x.strip()]

    def _split_by_symbol(self, cmd):
        for x in symbol:
            cmd = cmd.replace(x, " %s " % x)
        return cmd.split(" ")


if __name__ == '__main__':
    import sys

    fn = sys.argv[1]
    tokenizer = JackTokenizer(fn)
    out_file = fn.split("/")[-1].split("\\")[-1][:-5] + "T.xml"
    from lxml import etree as et

    doc = et.Element("tokens")
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        if tokenizer.token_type() == TokenType.keyword:
            ele = et.Element("keyword")
            ele.text = tokenizer.keyword().name.lower()
            doc.append(ele)
        elif tokenizer.token_type() == TokenType.symbol:
            ele = et.Element("symbol")
            ele.text = tokenizer.symbol()
            doc.append(ele)
        elif tokenizer.token_type() == TokenType.identifier:
            ele = et.Element("identifier")
            ele.text = tokenizer.identifier()
            doc.append(ele)
        elif tokenizer.token_type() == TokenType.intConstant:
            ele = et.Element("integerConstant")
            ele.text = str(tokenizer.intVal())
            doc.append(ele)
        elif tokenizer.token_type() == TokenType.stringConstant:
            ele = et.Element("stringConstant")
            ele.text = tokenizer.stringVal()
            doc.append(ele)
    with open(out_file, "w+") as f:
        f.write(et.tostring(doc, pretty_print=True).decode("utf-8"))
