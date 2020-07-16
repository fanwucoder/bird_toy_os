//function SimpleFunction.test 2
(SimpleFunction.test)
@0 //0
D=A //1
@SP //2
A=M //3
M=D //4
@SP //5
M=M+1 //6
@0 //7
D=A //8
@SP //9
A=M //10
M=D //11
@SP //12
M=M+1 //13
//push local 0
@0 //14
D=A //15
@LCL //16
A=M+D //17
D=M //18
@SP //19
A=M //20
M=D //21
@SP //22
M=M+1 //23
//push local 1
@1 //24
D=A //25
@LCL //26
A=M+D //27
D=M //28
@SP //29
A=M //30
M=D //31
@SP //32
M=M+1 //33
//add
@SP //34
M=M-1 //35
A=M //36
D=M //37
@SP //38
M=M-1 //39
A=M //40
A=M //41
D=A+D //42
@SP //43
A=M //44
M=D //45
@SP //46
M=M+1 //47
//not
@SP //48
M=M-1 //49
A=M //50
D=M //51
D=!D //52
@SP //53
A=M //54
M=D //55
@SP //56
M=M+1 //57
//push argument 0
@0 //58
D=A //59
@ARG //60
A=M+D //61
D=M //62
@SP //63
A=M //64
M=D //65
@SP //66
M=M+1 //67
//add
@SP //68
M=M-1 //69
A=M //70
D=M //71
@SP //72
M=M-1 //73
A=M //74
A=M //75
D=A+D //76
@SP //77
A=M //78
M=D //79
@SP //80
M=M+1 //81
//push argument 1
@1 //82
D=A //83
@ARG //84
A=M+D //85
D=M //86
@SP //87
A=M //88
M=D //89
@SP //90
M=M+1 //91
//sub
@SP //92
M=M-1 //93
A=M //94
D=M //95
@SP //96
M=M-1 //97
A=M //98
A=M //99
D=A-D //100
@SP //101
A=M //102
M=D //103
@SP //104
M=M+1 //105
//return
// R13=FRAME=LCL
@LCL //106
D=M //107
@R13 //108
M=D //109
//RET=*(FRAME-5)
@5 //110
A=D-A //111
D=M //112
@R14 //113
M=D //114
//*ARG=POP()
@SP //115
M=M-1 //116
A=M //117
D=M //118
@ARG //119
A=M //120
M=D //121
//SP=ARG+1
@ARG //122
D=M+1 //123
@SP //124
M=D //125
//THAT=*(FRAME-1)
@R13 //126
M=M-1 //127
A=M //128
D=M //129
@THAT //130
M=D //131
//THIS=*(FRAME-2)
@R13 //132
M=M-1 //133
A=M //134
D=M //135
@THIS //136
M=D //137
//ARG=*(FRAME-3)
@R13 //138
M=M-1 //139
A=M //140
D=M //141
@ARG //142
M=D //143
//LCL=*(FRAME-4)
@R13 //144
M=M-1 //145
A=M //146
D=M //147
@LCL //148
M=D //149
//GOTO RET
@R14 //150
A=M //151
0;JMP //152
