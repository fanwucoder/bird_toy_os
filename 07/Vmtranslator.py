# coding=utf-8
from io import IOBase
import sys

if sys.version_info.major == 3:
    unicode = str
    from io import TextIOWrapper

    file = TextIOWrapper


class Parser(object):
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
        if self.command in archmetic:
            return Parser.C_ARITHMETIC
        if "push" in self.command:
            return Parser.C_PUSH
        if "pop" in self.command:
            return Parser.C_POP

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


class CodeWriter(object):
    def __init__(self, out_file):
        self.out_file = out_file
        self.filename = self.out_file.split("/")[-1][:-4]
        self.filename = self.filename.split("\\")[-1]
        self.outwrite = open(out_file, "w+")
        self.is_close = False
        self._label = 0
        self._static_label = 0

    def setFileName(self, filename):
        self.out_file = filename
        if not self.is_close:
            raise Exception("%s  opened!" % self.out_file)
        self.outwrite = open(self.out_file, "wb+")

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
            self._writeArithmetic(asm_command)
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
        self._writeArithmetic(asm_command)

    def writePushPop(self, commond, segment, index):
        asm_command = ""
        seg_map = {"argument": "ARG", "local": "LCL", "this": "THIS", "that": "THAT", "pointer": "3", "temp": "5"}
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
            self._writeArithmetic(asm_command)

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
            self._writeArithmetic(asm_command)

    def close(self):
        self.outwrite.close()
        self.is_close = True

    def _get_label(self):
        label = "j_label_%s" % self._label
        self._label += 1
        return label

    def _writeArithmetic(self, asm_command):
        lines = [x.strip() + "\n" for x in asm_command.split("\n") if x.strip()]
        self.outwrite.writelines(lines)

    def _get_static_label(self, index):
        label = "%s.%s" % (self.filename, index)
        return label

    def write_source_comment(self, command):
        self.outwrite.write("//%s\n" % command)


def translate(param):
    parser = Parser(param)
    out_file = param[:-3] + ".asm"
    writer = CodeWriter(out_file)
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
    writer.close()


if __name__ == '__main__':
    import sys

    translate(sys.argv[1])
