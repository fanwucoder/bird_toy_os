class Parser(object):
    def __init__(self, file, input=None):
        self._file = file
        self._input = input
        self._init_()

    def _init_(self):
        pass

    def hasMoreCommands(self):
        pass

    def advance(self):
        pass

    def commandType(self):
        pass

    def symbol(self):
        pass

    def dest(self):
        pass

    def comp(self):
        pass

    def jmp(self):
        pass


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
