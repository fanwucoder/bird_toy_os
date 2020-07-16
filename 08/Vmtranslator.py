# coding=utf-8
import os
import re
from io import IOBase, StringIO
import sys

if sys.version_info.major == 3:
    unicode = str
    from io import TextIOWrapper

    file = TextIOWrapper


class Parser(object):
    C_IF = "C_IF"
    C_GOTO = "C_GOTO"
    C_LABEL = "C_LABEL"
    C_POP = "C_POP"
    C_PUSH = "C_PUSH"
    C_ARITHMETIC = "C_ARITHMETIC"
    C_RETURN = "C_RETURN"
    C_FUNCTION = "C_FUNCTION"
    C_CALL = "C_CALL"

    def __init__(self, filename=None):

        self._file = filename
        self._buf = None
        self._advance = None  # type: str
        self._next_line = 0
        self.line = 0
        self.parts = []
        self.command = None  # type: str
        self._init_()

    def _init_(self):
        if isinstance(self._file, str) or isinstance(self._file, unicode):
            self._buf = open(self._file, 'r')
        elif isinstance(self._file, file) or isinstance(self._file, IOBase):
            self._buf = self._file
        else:
            raise ValueError("file object show file or readable")

    def hasMoreCommands(self):

        if self._advance:
            return True
        while True:
            # 跳过注释
            line = self._buf.readline()
            if not line:
                return False
            self._next_line += 1
            if line.startswith("//") or line.strip() == "":
                continue
            if line:
                if "//" in line:
                    line = line.split("//")[0]
                self._advance = line.strip().replace("\n", "")
                return True

    def advance(self):
        if self.hasMoreCommands():
            self.line = self._next_line
            self.command = self._advance
            self._advance = None
            self.parts = [x for x in self.command.split(" ") if x != " "]
            print(self.line, self.command)
        else:
            raise ValueError("has no command.*")

    def commandType(self):
        archmetic = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
        if self.command.strip() in archmetic:
            return Parser.C_ARITHMETIC
        elif self.command.startswith("push "):
            return Parser.C_PUSH
        elif self.command.startswith("pop "):
            return Parser.C_POP
        elif self.command.startswith("function "):
            return Parser.C_FUNCTION
        elif self.command.startswith("label "):
            return Parser.C_LABEL
        elif self.command.startswith("goto "):
            return Parser.C_GOTO
        elif self.command.startswith("if-goto "):
            return Parser.C_IF
        elif self.command.startswith("call "):
            return Parser.C_CALL
        elif self.command.strip() == "return":
            return Parser.C_RETURN
        else:
            raise ValueError("unknow command %s" % self.command)

    def arg1(self):
        if self.commandType() == self.C_RETURN:
            raise ValueError("C_RETURN can not call this!")
        if self.commandType() == self.C_ARITHMETIC:
            return self.parts[0]
        else:
            return self.parts[1]

    def arg2(self):
        if self.commandType() in [self.C_POP, self.C_PUSH, self.C_FUNCTION, self.C_CALL]:
            return self.parts[2]
        raise ValueError("%s can not call this!" % self.commandType())


def _check_label(label):
    if not re.match("[A-Za-z_.:][A-Za-z_.:0-9]*", label):
        raise ValueError("%s is valid!")


class CodeWriter(object):
    def __init__(self, out_file):
        self.out_file = out_file
        self.filename = self.out_file.split("/")[-1][:-4]
        self.filename = self.filename.split("\\")[-1]
        self.outwrite = open(out_file, "w+")
        self.is_close = False
        self._curr_func = None
        self._label = 0
        self._static_label = 0

    def setFileName(self, filename):
        self.out_file = filename
        if not self.is_close:
            raise Exception("%s  opened!" % self.out_file)
        self.outwrite = open(self.out_file, "w+")

    def write_init(self):
        # SP=256
        self._write_asm("""
        @256
        D=A
        @R0
        M=D
        """)
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        _check_label(label)
        label = self._get_func_label(label)
        self._write_label(label)

    def _write_label(self, label):
        self._write_asm("""
        ({label})
        """.format(label=label))

    def write_goto(self, label):
        _check_label(label)
        label = self._get_func_label(label)
        self._write_goto(label)

    def _write_goto(self, label):
        self._write_asm("""
        @{label}
        0;JMP
        """.format(label=label))

    def write_if(self, label):
        _check_label(label)
        label = self._get_func_label(label)
        self._write_asm("""
         @SP
         M=M-1
         A=M
         D=M
         @{label}
         D;JNE
        """.format(label=label))

    def _push_ram(self, index=0, base=None):
        """
        存取任意ram的数据
        :param base:
        :param index:
        :return:
        """
        if base is None:
            addr = index
            asm_command = """
            @{addr}
            A=M
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """.format(addr=addr)
            self._write_asm(asm_command)

    def write_call(self, functionName, numArgs):
        return_addr = self._get_label()
        self.writePushPop(Parser.C_PUSH, "constant", return_addr)
        self._push_ram(1)
        self._push_ram(2)
        self._push_ram(3)
        self._push_ram(4)
        # ARG=SP-n-5
        self._write_asm("""
        @SP
        D=M
        @{numArgs}
        D=D-A
        @5
        D=D-A
        @ARG
        M=D
        """.format(numArgs=numArgs))
        # LCL=SP
        self._write_asm("""
        @SP
        D=M
        @LCL
        M=D
        """)
        self._write_goto(functionName)
        self._write_label(return_addr)

    def write_return(self):
        # self._curr_func = None
        self._write_asm("""
        // R13=FRAME=LCL
        @LCL
        D=M
        @R13
        M=D
        //RET=*(FRAME-5)
        @5
        A=D-A
        D=M
        @R14
        M=D
        //*ARG=POP() 
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D
        //SP=ARG+1
        D=D+1
        @SP
        M=D
        //THAT=*(FRAME-1)
        @R13
        D=M-1
        @THAT
        M=D
        //THIS=*(FRAME-2)
        D=D-1
        @THIS
        M=D
        //ARG=*(FRAME-3)
        D=D-1
        @ARG
        M=D
        //LCL=*(FRAME-4)
        D=D-1
        @LCL
        M=D
        //GOTO RET
        @R14
        0;JMP
        """)

    def write_function(self, functionName, numLocals):
        self._curr_func = functionName
        self._write_label(functionName)
        for i in range(numLocals):
            self.writePushPop(Parser.C_PUSH, "constant", 0)

    def writeArithmetic(self, command):
        pop_type = 0
        # [SP]=D
        asm_command = """
         @SP
         M=M-1
         A=M
         D=M
        """
        # 将D=[SP]
        end_command = """
        @SP
        A=M
        M=D
        @SP
        M=M+1        
        """
        if command == "neg":
            asm_command += """
            D=-D    
            """
            pop_type = 1
        if command == "not":
            asm_command += """
            D=!D    
            """
            pop_type = 1
        if pop_type == 1:
            asm_command += end_command
            self._write_asm(asm_command)
            return
        # SP=SP-1,取栈顶元素
        # A=[SP]
        asm_command += """
        @SP
        M=M-1
        A=M
        A=M
        """
        if command == "add":
            asm_command += """                                 
                    D=A+D
            """
        if command == "sub":
            asm_command += """                                 
                      D=A-D
              """
        if command == "and":
            asm_command += """                                 
                D=A&D                   
               """
        if command == "or":
            asm_command += """                                 
                      D=A|D              
               """

        label1 = self._get_label()
        label2 = self._get_label()
        compare_tp = """                                 
                      D=A-D
                      @{label1}
                      D;{jump}
                      D=0
                      @{label2}
                      0;JMP
                      ({label1})
                      D=-1
                      ({label2})                      
              """
        if command == "eq":
            asm_command += compare_tp.format(label1=label1, label2=label2, jump="JEQ")
        if command == "gt":
            asm_command += compare_tp.format(label1=label1, label2=label2, jump="JGT")

        if command == "lt":
            asm_command += compare_tp.format(label1=label1, label2=label2, jump="JLT")

        asm_command += end_command
        self._write_asm(asm_command)

    def writePushPop(self, commond, segment, index):
        asm_command = ""
        seg_map = {"argument": "ARG", "local": "LCL", "this": "THIS", "that": "THAT", "pointer": "3", "temp": "5",
                   "_call_seg": "0"}
        if commond == Parser.C_PUSH:
            if segment == "constant":
                asm_command += """
                    @{index}
                    D=A
                """.format(index=index)
            else:
                tmp = ""
                if segment in seg_map:
                    tmp = """
                    @{index}
                    D=A
                    @{seg}
                    A=M+D
                    D=M
                    """.format(index=index, seg=seg_map[segment])
                if segment in ["pointer", "temp"]:
                    tmp = tmp.replace("A=M+D", "A=A+D")
                if segment == "static":
                    label = self._get_static_label(index)
                    tmp = """
                    @{label}
                    D=M
                    """.format(label=label)
                asm_command += tmp
            asm_command += """
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
            self._write_asm(asm_command)

            return
        # todo R13被用来保存入栈内存地址，直接使用的，并没有做保存和恢复
        if commond == Parser.C_POP:
            tmp = ""
            if segment in seg_map:
                tmp = """
                @{index}
                D=A
                @{seg}
                D=M+D
                @R13
                M=D
                """.format(index=index, seg=seg_map[segment])
            if segment in ["pointer", "temp"]:
                tmp = tmp.replace("D=M+D", "D=A+D")
            if segment == "static":
                label = self._get_static_label(index)
                # 直接将xxx.j的地址保存到R13当中,让所有的pop和push命令统一，可能会造成代码过长
                tmp = """
                       @{label}
                       D=A
                       @R13
                       M=D
                """.format(label=label)
            asm_command += tmp
            asm_command += """
            @SP
            M=M-1
            A=M
            D=M
            @R13
            A=M
            M=D
            """
            self._write_asm(asm_command)

    def close(self):
        self.outwrite.close()
        self.is_close = True

    def _get_label(self):
        label = "j_label_%s" % self._label
        self._label += 1
        return label

    def _write_asm(self, asm_command):
        lines = [x.strip() + "\n" for x in asm_command.split("\n") if x.strip()]
        self.outwrite.writelines(lines)

    def _get_static_label(self, index):
        label = "%s.%s" % (self.filename, index)
        return label

    def write_source_comment(self, command):
        self.outwrite.write("//%s\n" % command)

    def _get_func_label(self, label):
        label = self._curr_func + "$" + label
        return label


def translate(param):
    if os.path.isdir(param):
        files = [os.path.join(param, x) for x in os.listdir(param) if x.endswith(".vm")]
    else:
        files = [param]
    writer = None
    for f in files:
        parser = Parser(f)
        out_file = f[:-3] + ".asm"
        if writer is None:
            writer = CodeWriter(out_file)
            writer.write_init()
        else:
            writer.close()
            writer.setFileName(out_file)
        while parser.hasMoreCommands():
            parser.advance()
            ct = parser.commandType()
            writer.write_source_comment(parser.command)
            if ct == Parser.C_ARITHMETIC:
                writer.writeArithmetic(parser.arg1())
            elif ct == Parser.C_PUSH:
                writer.writePushPop(Parser.C_PUSH, parser.arg1(), parser.arg2())
            elif ct == Parser.C_POP:
                writer.writePushPop(Parser.C_POP, parser.arg1(), parser.arg2())
            elif ct == Parser.C_LABEL:
                writer.write_label(parser.arg1())
            elif ct == Parser.C_GOTO:
                writer.write_goto(parser.arg1())
            elif ct == Parser.C_IF:
                writer.write_if(parser.arg1())
            elif ct == Parser.C_CALL:
                writer.write_call(parser.arg1(), int(parser.arg2()))
            elif ct == Parser.C_FUNCTION:
                writer.write_function(parser.arg1(),int( parser.arg2()))
            elif ct == Parser.C_RETURN:
                writer.write_return()
    writer.close()


if __name__ == '__main__':
    import sys

    translate(sys.argv[1])
