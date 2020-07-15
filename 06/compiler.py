# coding=utf-8
from io import IOBase
import re


class Parser(object):
    L_COMMAND = "L_COMMAND"
    C_COMMAND = "C_COMMAND"
    A_COMMAND = "A_COMMAND"

    def __init__(self, filename=None):

        self._file = filename
        self._buf = None
        self._advance = None  # type: str
        self._next_line = 0
        self.line = 0
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
            self._next_line += 1
            if line and line.startswith("//"):
                continue
            if line:
                self._advance = line
                return True
            else:
                return False

    def advance(self):
        if self.hasMoreCommands():
            self.line = self._next_line
            self.command = self._advance
            self._advance = None
        else:
            raise ValueError("has no command.*")

    def commandType(self):
        """
        简单的判断类型，此处不做正确性检查
        :return:
        """
        if self.command.startswith("@"):
            return self.A_COMMAND
        if "(" in self.command:
            return self.L_COMMAND
        if "=" in self.command:
            return self.C_COMMAND
        if ";" in self.command:
            return self.C_COMMAND

    def symbol(self):
        if re.match("\([a-zA-Z_\\.\\$\\:][a-zA-Z_\\.\\$\\:0-9]+\)", self.command):
            return self.command.replace("(", "").replace(")", "")
        else:
            raise ValueError("Syntax error:%s,%s" % (self.line, self.command))

    def dest(self):

        if "=" in self.command:
            dest = self.command.split('=')[0]
            if re.match("^[AMD]{1,3}$", dest):
                return dest
        raise ValueError("Syntax error:%s,%s" % (self.line, self.command))

    def comp(self):
        test_commnad = ["A", "-D", "-A", "D", "D+1", "U5", "U4", "A+1", "U6", "U1", "A-D", "U3", "U2", "D-1", "D|A",
                        "M+1",
                        "M-D", "M", "D|M", "U8", "!A", "D-A", "M+D", "!D", "!M", "D-M", "M-1", "1", "0", "-1", "-M",
                        "D+A", "A-1", "D&M", "D&A", "U7", ""]
        comp = None
        if ";" in self.command:
            comp = self.command.split(';')[0]
        if "=" in self.command:
            comp = self.command.split("=")[1]
        if comp in test_commnad:
            return comp
        raise ValueError("Syntax error:%s,%s" % (self.line, self.command))

    def jmp(self):
        jmp = None
        if ";" in self.command:
            jmp = self.command.split(';')[1]
        test_jmp = ["", 'JLT', 'JLE', 'JEQ', 'JNE', 'JGT', 'JGE', "JMP"]
        if jmp in test_jmp:
            return jmp
        raise ValueError("Syntax error:%s,%s" % (self.line, self.command))


class Code(object):
    def __init__(self):
        pass

    def dest(self, dest_code):
        code = ''
        code += '1' if 'A' in dest_code else '0'
        code += '1' if 'D' in dest_code else '0'
        code += '1' if 'M' in dest_code else '0'
        return code

    def comp(self, comp_code):
        test_table = {'0': '0101010',
                      '1': '0111111',
                      '-1': '0111010',
                      'D': '0001100',
                      'A': '0110000',
                      '!D': '0001101',
                      '!A': '0110001',
                      '-D': '0001111',
                      '-A': '0110011',
                      'D+1': '0011111',
                      'A+1': '0110111',
                      'D-1': '0001110',
                      'A-1': '0110010',
                      'D+A': '0000010',
                      'D-A': '0010011',
                      'A-D': '0000111',
                      'D&A': '0000000',
                      'D|A': '0010101',

                      # 'U1' :'1101010',
                      # 'U2' :'1111111',
                      # 'U3' :'1111010',
                      # 'U4' :'1001100',
                      'M': '1110000',
                      # 'U5' :'1001101',
                      '!M': '1110001',
                      # 'U6' :'1001111',
                      '-M': '1110011',
                      # 'U7' :'1011111',
                      'M+1': '1110111',
                      # 'U8' :'1001110',
                      'M-1': '1110010',
                      'M+D': '1000010',
                      'D-M': '1010011',
                      'M-D': '1000111',
                      'D&M': '1000000',
                      'D|M': '1010101',
                      }
        return test_table.get(comp_code, None)

    def jump(self, jump_code):
        jump_map = {
            # "":   '000',
            "JGT": '001',
            "JEQ": '010',
            "JGE": '011',
            "JLT": '100',
            "JNE": '101',
            "JLE": '110',
            "JMP": '111'
        }
        return jump_map.get(jump_code, None)


class SymbolTable(object):
    def __init__(self):
        pass
        self._label = dict()

    def addEntry(self, symbol, addr):
        self._label[symbol] = addr

    def contains(self, symbol):
        return symbol in self._label

    def getAddress(self, symbol):
        return self._label[symbol]
