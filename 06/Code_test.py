import unittest
from compiler import Code
class TestCode(unittest.TestCase):
    def setUp(self):
        self.code=Code()
        return super().setUp()

    def test_comp(self):
        test_table={'0'  :'0101010',
                    '1'  :'0111111',
                    '-1' :'0111010',
                    'D'  :'0001100',
                    'A'  :'0110000',
                    '!D' :'0001101',
                    '!A' :'0110001',
                    '-D' :'0001111',
                    '-A' :'0110011',
                    'D+1':'0011111',
                    'A+1':'0110111',
                    'D-1':'0001110',
                    'A-1':'0110010',
                    'D+A':'0000010',
                    'D-A':'0010011',
                    'A-D':'0000111',
                    'D&A':'0000000',
                    'D|A':'0010101',

                    'U1' :'1101010',
                    'U2' :'1111111',
                    'U3' :'1111010',
                    'U4' :'1001100',
                    'M'  :'1110000',
                    'U5' :'1001101',
                    '!M' :'1110001',
                    'U6' :'1001111',
                    '-M' :'1110011',
                    'U7' :'1011111',
                    'M+1':'1110111',
                    'U8' :'1001110',
                    'M-1':'1110010',
                    'M+D':'1000010',
                    'D-M':'1010011',
                    'M-D':'1000111',
                    'D&M':'1000000',
                    'D|M':'1010101',
                    }
        for k,v in test_table.items():
            if not k.startswith("U"):
                self.assertEqual(self.code.comp(k),v)

    def test_jump(self):
        jump_map={
            "":   '000',
            "JGT":'001',
            "JEQ":'010',
            "JGE":'011',
            "JLT":'100',
            "JNE":'101',
            "JLE":'110',
            "JMP":'111'
        }
        for k,v in jump_map.items():
            if k!="":
                self.assertEqual(self.code.jump(k),v)
    def test_dest(self):
        print()
        for i in range(2):
            dest1='A' if i==0 else ''
            code1='1' if i==0 else '0'
            for j in range(2):
                dest2=dest1+('D' if i==0 else '')
                code2=code1+('1' if i==0 else '0')
                for k in range(2):
                    dest=dest2+('M' if i==0 else '')
                    code=code2+('1' if i==0 else '0')
                    code_ret=self.code.dest(dest)
                    print(code,dest,code_ret)
                    # print(dest)
                    self.assertEqual(code_ret,code)
            
if __name__ == '__main__':
    unittest.main()
