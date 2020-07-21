import sys
from io import IOBase

from lxml import etree as et

from JackTokenizer import JackTokenizer, TokenType, KeywordType
from SymbolTable import SymbolTable
from VMWriter import VMWriter

SEG_CONSTANT = "constant"
SEG_POINTER = "pointer"
SEG_LOCAL = "local"
SEG_STATIC = "static"
SEG_THAT = "that"
SEG_THIS = "this"
SEG_TEMP = "temp"
SEG_ARG = "argument"
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
        self._n_args = []
        self._root = None
        self.class_name = None
        self.return_type = None
        self._label_cnt = 0
        self.vm_writer = None  # type:VMWriter
        self._init()
        self.symbol = SymbolTable()

    def _init(self):
        self._inputbuf = self.create_buffer(self._inputfile)
        self._outputbuf = self.create_buffer(self._outputfile, mode="w+")
        self.vm_writer = VMWriter(self._outputfile[:-4] + ".vm")
        self._tokenizer = JackTokenizer(self._inputbuf)

    def create_buffer(self, fn, mode='r'):

        if isinstance(fn, str) or isinstance(fn, unicode):
            return open(fn, mode)
        elif isinstance(fn, file) or isinstance(fn, IOBase):
            return fn
        else:
            raise ValueError("file object show file or readable")

    def compile_class(self):
        parent = self._set_parent("class")
        self._root = parent
        self._advance()
        self._pop_required(parent, TokenType.keyword, KeywordType.CLASS)
        self.class_name = self._token()[1]
        self._pop_required(parent, TokenType.identifier)
        self._pop_required(parent, TokenType.symbol, "{")

        try:
            while self._is_class_var():
                self.compile_class_var_desc()

            while self._is_subroutine():
                self.compile_subroutine()
            self._pop_required(parent, TokenType.symbol, "}")
            print(self.symbol)
        finally:
            self._outputbuf.write(unicode(et.tostring(self._root, pretty_print=True, method="c14n2").decode("utf-8")))
            self.vm_writer.close()
        self._outputbuf.close()

    def _required_type(self, token_type, val=None):
        tp, tv = self._token()
        if token_type != tp or ((tp == TokenType.keyword or tp == TokenType.symbol) and (val != tv)):
            raise ValueError("token must be %s,%s" % (token_type, val))
        return tp, tv

    def compile_class_var_desc(self):
        parent = self._set_parent("classVarDec")
        # 具体可以细分变量类型检查，标识符正确检查
        parent.append(self._build_element())
        kind = self.get_kind()
        self._advance()
        itype = self.get_type()
        parent.append(self._build_element())
        self._advance()

        while not self.is_token(TokenType.symbol, ";"):
            parent.append(self._build_element())
            if self._token()[1] != "," and self._token()[1] != ";":
                self.symbol.define(self._token()[1], itype, kind)
            self._advance()
        parent.append(self._build_element())
        self._advance()
        self._remove_parent()

    def get_kind(self):
        kind = self._token()[1]
        if isinstance(kind, KeywordType):
            kind = kind.name.lower()
        return kind

    def get_type(self):
        itype = self._token()[1]
        if isinstance(itype, KeywordType):
            return itype.name.lower()
        return itype

    def compile_subroutine(self):
        print(self.symbol)
        self.symbol.start_subroutine()
        parent = self._set_parent("subroutineDec")
        method_type = self._token()[1]
        self._advance()
        self.return_type = self._token()[1]
        self._advance()
        function_name = self._token()[1]
        self._advance()
        self._pop_required(parent, TokenType.symbol, "(")
        self.compile_parameter_list()
        full_name = "{}.{}".format(self.class_name, function_name)

        self._pop_required(parent, TokenType.symbol, ")")
        self._compile_body(full_name, method_type)
        self._remove_parent()
        self.vm_writer.write_comment("end function %s" % function_name)
        self.vm_writer.write_comment("")
        # if self._tokenizer.token_type()==TokenType.KEY_WORD:

    def _compile_body(self, full_name, method_type):
        parent = self._set_parent("subroutineBody")
        self._pop_required(parent, TokenType.symbol, "{")
        while self._is_var_desc():
            self.compile_var_desc()

        var_cnt = self.symbol.var_count("var")
        field_cnt = self.symbol.var_count("field")
        self.vm_writer.write_function(full_name, var_cnt)
        if method_type == KeywordType.CONSTRUCTOR:
            #  构造函数分配对象内存
            self.vm_writer.write_push(SEG_CONSTANT, field_cnt)
            self.vm_writer.write_call("Memory.alloc", "1")
            self.vm_writer.write_pop(SEG_POINTER, "0")
        elif method_type == KeywordType.METHOD:
            # 成员方法，设置this=arg[0]
            self.vm_writer.write_push(SEG_ARG, "0")
            self.vm_writer.write_pop(SEG_POINTER, "0")
        self.compile_statements()
        self._pop_required(parent, TokenType.symbol, "}")
        self._remove_parent()

    def _remove_parent(self):
        self._cur_root.pop()

    def compile_parameter_list(self):
        kind = "arg"
        while not self.is_token(TokenType.symbol, ")"):
            itype = self.get_type()
            self._advance()
            name = self._token()[1]
            self.symbol.define(name, itype, kind)
            self._advance()
            # parent.append(self._build_element())
            if self.is_token(TokenType.symbol, ","):
                self._advance()

    def compile_var_desc(self):
        parent = self._set_parent("varDec")
        self._pop_required(parent, TokenType.keyword, KeywordType.VAR)
        kind = "var"
        itype = self.get_type()
        parent.append(self._build_element())
        self._advance()

        while not self.is_token(TokenType.symbol, ";"):
            # parent.append(self._build_element())
            if not self.is_token(TokenType.symbol, ",") and not self.is_token(TokenType.symbol, ";"):
                self.symbol.define(self._token()[1], itype, kind)
            self._advance()
        self._pop_required(parent, TokenType.symbol, ";")
        self._remove_parent()

    def compile_statements(self):

        self._set_parent("statements")

        while self._is_statement():
            if self.is_let_statement():
                self.compile_let()
            if self.is_do_statement():
                self.compile_do()
            if self.is_return_statement():
                self.compile_return()
            if self.is_if_statement():
                self.compile_if()
                continue
            if self.is_while_statement():
                self.compile_while()
                continue
        self._remove_parent()

    def compile_do(self):
        parent = self._set_parent("doStatement")
        self._pop_required(parent, TokenType.keyword, KeywordType.DO)
        type1, id1 = self._pop_required(parent, TokenType.identifier)
        self.compile_call(type1, id1)
        self.vm_writer.write_pop(SEG_TEMP, 0)
        self._pop_required(parent, TokenType.symbol, ";")
        self._remove_parent()

    def compile_call(self, typ1, id1):
        parent = None
        symbol_kind = self.symbol.kind_of(id1)
        # 调用变量方法
        n_args = 0
        typ2, id2 = self._token()
        if id2 == ".":
            if symbol_kind:
                # 变量类型
                function_type = self.symbol.type_of(id1)
                # this 指针入栈
                if symbol_kind == "arg":
                    self.vm_writer.write_push("argument", self.symbol.index_of(id1))
                elif symbol_kind == "static":
                    self.vm_writer.write_push("static", self.symbol.index_of(id1))
                elif symbol_kind == "var":
                    self.vm_writer.write_push("local", self.symbol.index_of(id1))
                elif symbol_kind == "field":
                    self.vm_writer.write_push("this", self.symbol.index_of(id1))
                n_args += 1
            else:
                # 静态方法
                function_type = id1
            self._advance()
            _, method_name = self._pop_required(parent, TokenType.identifier)
            full_name = "%s.%s" % (function_type, method_name)
        else:
            n_args += 1
            self.vm_writer.write_push("pointer", 0)
            function_type = self.class_name
            full_name = "%s.%s" % (function_type, id1)
        self._n_args.append(n_args)
        self._pop_required(parent, TokenType.symbol, "(")
        self.compile_expression_list()
        self._pop_required(parent, TokenType.symbol, ")")
        n_args = self._n_args.pop(-1)
        self.vm_writer.write_call(full_name, n_args=n_args)

    def compile_let(self):
        parent = self._set_parent("letStatement")
        self._pop_required(parent, TokenType.keyword, KeywordType.LET)
        tk, val = self._pop_required(parent, TokenType.identifier)
        seg, idx = self.get_var_seg_idx(val)
        is_arr = False
        if self.is_token(TokenType.symbol, "["):
            is_arr = True
            self._advance()
            self.compile_expression()
            self.vm_writer.write_push(seg, idx)
            self.vm_writer.write_arithmetic("+")
            self._pop_required(parent, TokenType.symbol, "]")

        # 有可能是数组
        # 替换正则
        self._pop_required(parent, TokenType.symbol, "=")
        self.compile_expression()
        if is_arr:
            self.vm_writer.write_pop(SEG_TEMP, "0")
            self.vm_writer.write_pop(SEG_POINTER, "1")
            self.vm_writer.write_push(SEG_TEMP, "0")
            self.vm_writer.write_pop(SEG_THAT, "0")
        else:
            self.vm_writer.write_pop(seg, idx)
        self._pop_required(parent, TokenType.symbol, ";")
        self._remove_parent()

    def compile_while(self):
        self.vm_writer.write_comment("start while")
        parent = self._set_parent("whileStatement")
        self._pop_required(parent, TokenType.keyword, KeywordType.WHILE)
        label1 = self._get_label()
        self.vm_writer.write_label(label1)
        label2 = self._get_label()
        self._pop_required(parent, TokenType.symbol, "(")
        self.compile_expression()
        self.vm_writer.write_arithmetic("~")
        self._pop_required(parent, TokenType.symbol, ")")
        self.vm_writer.write_if(label2)
        self._pop_required(parent, TokenType.symbol, "{")
        self.compile_statements()
        self._pop_required(parent, TokenType.symbol, "}")
        self.vm_writer.write_goto(label1)
        self.vm_writer.write_label(label2)
        self._remove_parent()

        self.vm_writer.write_comment("end while")

    def compile_return(self):
        parent = self._set_parent("returnStatement")
        self._pop_required(parent, TokenType.keyword, KeywordType.RETURN)
        if not self.is_token(TokenType.symbol, ";"):
            self.compile_expression()
        self._pop_required(parent, TokenType.symbol, ";")
        if self.return_type == KeywordType.VOID:
            self.vm_writer.write_push(SEG_CONSTANT, 0)
        self.vm_writer.write_return()
        self._remove_parent()

    def compile_if(self):
        parent = self._set_parent("ifStatement")
        self.vm_writer.write_comment("compile if")
        self._pop_required(parent, TokenType.keyword, KeywordType.IF)
        self._pop_required(parent, TokenType.symbol, "(")
        label1 = self._get_label()
        label2 = self._get_label()
        self.compile_expression()
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if(label1)
        self._pop_required(parent, TokenType.symbol, ")")
        self._pop_required(parent, TokenType.symbol, "{")
        self.compile_statements()
        self._pop_required(parent, TokenType.symbol, "}")
        self.vm_writer.write_goto(label2)
        self.vm_writer.write_label(label1)
        if self.is_token(TokenType.keyword, KeywordType.ELSE):
            self._pop_required(parent, TokenType.keyword, KeywordType.ELSE)
            self._pop_required(parent, TokenType.symbol, "{")
            self.compile_statements()
            self._pop_required(parent, TokenType.symbol, "}")
        self.vm_writer.write_label(label2)
        self._remove_parent()

        self.vm_writer.write_comment(" if end")

    def compile_expression(self):
        parent = self._set_parent("expression")
        op_count = 0
        ops = []
        while not self._is_end():
            self.compile_term()
            if self._is_op(False):
                _, op = self._token()
                self._advance()
                ops.append(op)
            op_count += 1
            if op_count >= 2:
                print(ops)
                self.vm_writer.write_arithmetic(ops.pop(0))
            # parent.append(self._build_element())
            # self._advance()

        self._remove_parent()

    def compile_term(self):
        parent = self._set_parent("term")
        first = True
        while not self._is_op(first) and not self._is_end():
            first = False
            if self.is_token(TokenType.symbol, "("):
                self._advance()
                self.compile_expression()
                self._pop_required(parent, TokenType.symbol, ")")

            elif self._is_unary_op():
                token, op = self._token()
                self._advance()
                op = "neg" if op == "-" else op
                self.compile_term()
                self.vm_writer.write_arithmetic(op)
                continue
            elif self.is_token(TokenType.identifier):
                tk, val = self._pop_required(parent, TokenType.identifier)
                if self.is_token(TokenType.symbol, "(") or self.is_token(TokenType.symbol, "."):
                    self.compile_call(tk, val)
                elif self.is_token(TokenType.symbol, "["):
                    self._advance()
                    self.compile_expression()
                    seg, idx = self.get_var_seg_idx(val)
                    self.vm_writer.write_push(seg, idx)
                    # 数组直接计算基址，通过that[0]访问
                    # fixme a[0] 这种常数的访问
                    self.vm_writer.write_arithmetic("+")
                    self.vm_writer.write_pop(SEG_POINTER, "1")
                    self.vm_writer.write_push(SEG_THAT, "0")
                    self._pop_required(parent, TokenType.symbol, "]")
                else:
                    # 变量
                    seg, idx = self.get_var_seg_idx(val)
                    self.vm_writer.write_push(seg, idx)
            else:
                tk, val = self._token()
                if self.is_token(TokenType.integerConstant):
                    self.vm_writer.write_push(SEG_CONSTANT, val)
                elif self.is_token(TokenType.keyword, KeywordType.TRUE):
                    self.vm_writer.write_push(SEG_CONSTANT, "0")
                    self.vm_writer.write_arithmetic("~")
                elif self.is_token(TokenType.keyword, KeywordType.FALSE):
                    self.vm_writer.write_push(SEG_CONSTANT, "0")
                elif self.is_token(TokenType.keyword, KeywordType.NULL):
                    self.vm_writer.write_push(SEG_CONSTANT, "0")
                elif self.is_token(TokenType.keyword, KeywordType.THIS):
                    self.vm_writer.write_push(SEG_POINTER, "0")
                elif self.is_token(TokenType.stringConstant):
                    str_len = len(val)
                    self.vm_writer.write_push(SEG_CONSTANT, str(str_len))
                    self.vm_writer.write_call("String.new", "1")

                    for idx, x in enumerate(val):
                        self.vm_writer.write_push(SEG_CONSTANT, str(ord(x)))
                        self.vm_writer.write_call("String.appendChar", '2')

                self._advance()
        self._remove_parent()

    def _pop_required(self, parent, tk, val=None):
        tk, val = self.required(tk, val)
        self._advance()
        return tk, val

    def _is_op(self, first):
        tk, val = self._token()
        return tk == TokenType.symbol and val in '+*/&|<>=' or (val == '-' and not first)

    def _is_unary_op(self):
        tk, val = self._token()
        return tk == TokenType.symbol and val in '-~'

    def compile_expression_list(self):
        parent = self._set_parent("expressionList")
        n_args = self._n_args[-1]
        while not self.is_token(TokenType.symbol, ")"):
            n_args += 1
            self.compile_expression()
            if self.is_token(TokenType.symbol, ","):
                self._pop_required(parent, TokenType.symbol, ",")
        self._n_args[-1] = n_args
        self._remove_parent()

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
        # if self._tokenizer.line > 44:
        #     raise ValueError("测试代码，翻译到此停止")
        token_type = self._tokenizer.token_type()
        if self._tokenizer.token_type() == TokenType.keyword:
            a, b = token_type, self._tokenizer.keyword()
        elif self._tokenizer.token_type() == TokenType.symbol:
            a, b = token_type, self._tokenizer.symbol()
        elif self._tokenizer.token_type() == TokenType.identifier:
            a, b = token_type, self._tokenizer.identifier()
        elif self._tokenizer.token_type() == TokenType.integerConstant:
            a, b = token_type, self._tokenizer.intVal()
        elif self._tokenizer.token_type() == TokenType.stringConstant:
            a, b = token_type, self._tokenizer.stringVal()
        else:
            a, b = None, None
        # print(a, b, self._tokenizer.line)
        return a, b

    def _advance(self):
        if self._tokenizer.has_more_tokens():
            self._tokenizer.advance()

    def required(self, token, val=None):
        return self._required_type(token, val)

    def _build_element(self):
        a, b = self._token()
        e = et.Element(a.name)
        if isinstance(b, KeywordType):
            e.text = b.name.lower()
        else:
            e.text = b
        return e

    def _is_class_var(self):
        return self.is_token(TokenType.keyword, KeywordType.FIELD) or self.is_token(TokenType.keyword,
                                                                                    KeywordType.STATIC)

    def is_token(self, token, val=None):
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
        return self.is_token(TokenType.keyword, KeywordType.FUNCTION) \
               or self.is_token(TokenType.keyword, KeywordType.CONSTRUCTOR) \
               or self.is_token(TokenType.keyword, KeywordType.METHOD)

    def _is_statement(self):
        if self.is_let_statement():
            return True
        if self.is_do_statement():
            return True
        if self.is_return_statement():
            return True
        if self.is_if_statement():
            return True
        if self.is_while_statement():
            return True

    def is_while_statement(self):
        return self.is_token(TokenType.keyword, KeywordType.WHILE)

    def is_let_statement(self):
        return self.is_token(TokenType.keyword, KeywordType.LET)

    def is_do_statement(self):
        return self.is_token(TokenType.keyword, KeywordType.DO)

    def is_return_statement(self):
        return self.is_token(TokenType.keyword, KeywordType.RETURN)

    def is_if_statement(self):
        return self.is_token(TokenType.keyword, KeywordType.IF)

    def _is_var_desc(self):
        return self.is_token(TokenType.keyword, KeywordType.VAR)

    def _is_end(self):
        return self.is_token(TokenType.symbol, ";") or \
               self.is_token(TokenType.symbol, ";") \
               or self.is_token(TokenType.symbol, ")") \
               or self.is_token(TokenType.symbol, ",") \
               or self.is_token(TokenType.symbol, "]")

    def get_var_seg_idx(self, val):
        kind = self.symbol.kind_of(val)
        idx = self.symbol.index_of(val)
        if kind == "static":
            return SEG_STATIC, idx
        elif kind == "var":
            return SEG_LOCAL, idx
        elif kind == "field":
            return SEG_THIS, idx
        elif kind == "arg":
            return SEG_ARG, idx

    def _get_label(self):
        label = "label_%s" % self._label_cnt
        self._label_cnt += 1
        return label


if __name__ == '__main__':
    import os

    dir = "TestString"
    for f in os.listdir(dir):
        if not f.endswith(".jack"):
            continue
        print(f)
        fn = os.path.join(dir, f)
        compiler = CompilationEngine(fn, fn[:-5] + ".xml")
        compiler.compile_class()
