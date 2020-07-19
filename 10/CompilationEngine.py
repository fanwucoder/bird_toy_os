import sys
from io import IOBase, StringIO
from lxml import etree as et
from lxml.etree import Element

from JackTokenizer import JackTokenizer, TokenType, KeywordType

if sys.version_info.major == 3:
    unicode = str
    from io import TextIOWrapper

    file = TextIOWrapper


class CompilationEngine(object):
    def __init__(self, inputfile, outputfile):
        self._inputfile = inputfile
        self._outputfile = outputfile
        self._tokenizer: JackTokenizer = None
        self._cur_root = []
        self._root = None
        self._init()

    def _init(self):
        self._inputbuf = self.create_buffer(self._inputfile)
        self._outputbuf = self.create_buffer(self._outputfile, mode="w+")
        self._tokenizer = JackTokenizer(self._inputbuf)

    def create_buffer(self, fn, mode='r'):

        if isinstance(fn, str) or isinstance(fn, unicode):
            return open(fn, mode)
        elif isinstance(fn, file) or isinstance(fn, IOBase):
            return fn
        else:
            raise ValueError("file object show file or readable")

    def compile_class(self):
        self._advance()
        self._required_type(TokenType.keyWord, KeywordType.CLASS)
        parent = self._set_parent("class")
        self._root = parent
        self._tokenizer.advance()
        parent.append(self.required(TokenType.identifier))
        self._tokenizer.advance()
        parent.append(self.required(TokenType.symbol, "{"))
        self._advance()
        while self._is_class_var():
            self.compile_class_var_desc()
            self._advance()
        try:
            while self._is_subroutine():
                self.compile_subroutine()
                self._advance()
        finally:
            self._outputbuf.write(unicode(et.tostring(self._root, pretty_print=True).decode("utf-8")))

        self._outputbuf.close()

    def _required_type(self, token_type, val):
        tp, tv = self._token()
        if token_type != tp or ((tp == TokenType.keyWord or tp == TokenType.symbol) and (val != tv)):
            raise ValueError("token must be %s,%s" % (token_type, val))

    def compile_class_var_desc(self):
        parent = self._get_parent()
        ele = et.Element("classVarDec")
        parent.append(ele)
        self._set_parent("class")
        # 具体可以细分变量类型检查，标识符正确检查
        while not self.is_token(TokenType.symbol, ";"):
            ele.append(self._build_element())
            self._advance()
        ele.append(self._build_element())
        self.remove_parent()

    def compile_subroutine(self):
        parent = self._set_parent("subroutineDec")
        while True:
            parent.append(self._build_element())
            if self.is_token(TokenType.symbol, "("):
                break
            self._advance()
        self.compile_parameter_list()

        parent.append(self.required(TokenType.symbol, ")"))
        self._advance()

        self._compile_body()
        self.remove_parent()

        # if self._tokenizer.token_type()==TokenType.KEY_WORD:

    def _compile_body(self):
        parent = self._set_parent("subroutineBody")
        parent.append(self.required(TokenType.symbol, "{"))
        self.compile_statements()
        parent.append(self.required(TokenType.symbol, "}"))
        self.remove_parent()

    def remove_parent(self):
        self._cur_root.pop()

    def compile_parameter_list(self):
        parent = self._set_parent("parameterList")
        while not self.is_token(TokenType.symbol, ")"):
            parent.append(self._build_element())
            self._advance()
        self.remove_parent()

    def compile_var_desc(self):
        pass

    def compile_statements(self):

        self._set_parent("statements")
        self._advance()
        while self._is_statement():
            if self.is_let_statement():
                self.compile_let()
            if self.is_do_statement():
                self.compile_do()
            if self.is_return_statement():
                self.compile_return()
            if self.is_if_statement():
                self.compile_if()
            self._advance()

        self.remove_parent()

    def compile_do(self):
        parent = self._set_parent("doStatement")
        parent.append(self.required(TokenType.keyWord, KeywordType.DO))
        self._advance()
        while not self.is_token(TokenType.symbol, "("):
            parent.append(self._build_element())
            self._advance()
        parent.append(self.required(TokenType.symbol, "("))
        self.compile_expression_list()
        parent.append(self.required(TokenType.symbol, ")"))
        self._advance()
        parent.append(self.required(TokenType.symbol, ";"))
        self.remove_parent()

    def compile_let(self):
        parent = self._set_parent("letStatement")
        parent.append(self.required(TokenType.keyWord, KeywordType.LET))
        self._advance()
        parent.append(self.required(TokenType.identifier))
        self._advance()
        # 有可能是数组
        parent.append(self.required(TokenType.symbol, "="))
        self._advance()
        self.compile_expression()
        parent = self._get_parent()
        parent.append(self.required(TokenType.symbol, ";"))
        self.remove_parent()

    def compile_while(self):
        pass

    def compile_return(self):
        parent = self._set_parent("returnStatement")
        parent.append(self.required(TokenType.keyWord, KeywordType.RETURN))
        self._advance()
        self.compile_expression()
        parent.append(self.required(TokenType.symbol, ";"))
        self.remove_parent()

    def compile_if(self):
        parent = self._set_parent("ifStatement")
        parent.append(self.required(TokenType.keyWord, KeywordType.IF))
        self._advance()

    def compile_expression(self):
        parent = self._set_parent("expression")
        parent = self._set_parent("term")
        while not self.is_token(TokenType.symbol, ";"):
            parent.append(self._build_element())
            self._advance()
        self.remove_parent()
        self.remove_parent()

    def compile_term(self):
        pass

    def compile_expression_list(self):
        parent = self._set_parent("expressionList")
        while not self.is_token(TokenType.symbol, ")"):
            self._advance()
        self.remove_parent()

    def build_identifier(self):
        e = et.Element("identifier")
        e.text = self._tokenizer.identifier()
        return e

    def build_keyword(self):
        e = et.Element("keyword")
        e.text = self._tokenizer.keyword().name.lower()
        return e

    def build_symbol(self):
        e = et.Element("symbol")
        e.text = self._tokenizer.symbol()
        return e

    def _token(self):

        token_type = self._tokenizer.token_type()
        if self._tokenizer.token_type() == TokenType.keyWord:
            a, b = token_type, self._tokenizer.keyword()
        elif self._tokenizer.token_type() == TokenType.symbol:
            a, b = token_type, self._tokenizer.symbol()
        elif self._tokenizer.token_type() == TokenType.identifier:
            a, b = token_type, self._tokenizer.identifier()
        elif self._tokenizer.token_type() == TokenType.intConstant:
            a, b = token_type, self._tokenizer.intVal()
        elif self._tokenizer.token_type() == TokenType.stringConstant:
            a, b = token_type, self._tokenizer.stringVal()
        else:
            a, b = None, None
        print(a, b, self._tokenizer.line)
        return a, b

    def _advance(self):
        self._tokenizer.advance()

    def required(self, token, val=None):
        self._required_type(token, val)
        return self._build_element()

    def _build_element(self):
        a, b = self._token()
        e = et.Element(a.name)
        if isinstance(b, KeywordType):
            e.text = b.name.lower()
        else:
            e.text = b
        return e

    def _is_class_var(self):
        return self.is_token(TokenType.keyWord, KeywordType.FIELD) or self.is_token(TokenType.keyWord,
                                                                                    KeywordType.STATIC)

    def is_token(self, token, val):
        t, v = self._token()
        if val is not None:
            return t == token and v == val
        else:
            return t == token

    def _get_parent(self):
        if len(self._cur_root) > 0:
            return self._cur_root[-1]
        else:
            return None

    def _set_parent(self, name):
        parent = self._get_parent()
        ele2 = et.Element(name)
        if parent is not None:
            parent.append(ele2)
        self._cur_root.append(ele2)
        return ele2

    def _is_subroutine(self):
        return self.is_token(TokenType.keyWord, KeywordType.FUNCTION) \
               or self.is_token(TokenType.keyWord, KeywordType.CONSTRUCTOR) \
               or self.is_token(TokenType.keyWord, KeywordType.METHOD)

    def _is_statement(self):
        if self.is_let_statement():
            return True
        if self.is_do_statement():
            return True
        if self.is_return_statement():
            return True
        if self.is_if_statement():
            return True

    def is_let_statement(self):
        return self.is_token(TokenType.keyWord, KeywordType.LET)

    def is_do_statement(self):
        return self.is_token(TokenType.keyWord, KeywordType.DO)

    def is_return_statement(self):
        return self.is_token(TokenType.keyWord, KeywordType.RETURN)

    def is_if_statement(self):
        return self.is_token(TokenType.keyWord, KeywordType.IF)


if __name__ == '__main__':
    compiler = CompilationEngine("ExpressionLessSquare\\Square.jack", "Square.xml")
    compiler.compile_class()
