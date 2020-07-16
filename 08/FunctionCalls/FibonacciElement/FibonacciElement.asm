@256 //0
D=A //1
@R0 //2
M=D //3
//push return address
@j_label_0 //4
D=A //5
@SP //6
A=M //7
M=D //8
@SP //9
M=M+1 //10
//push LCL
@1 //11
A=M //12
D=A //13
@SP //14
A=M //15
M=D //16
@SP //17
M=M+1 //18
//push ARG
@2 //19
A=M //20
D=A //21
@SP //22
A=M //23
M=D //24
@SP //25
M=M+1 //26
//push THIS
@3 //27
A=M //28
D=A //29
@SP //30
A=M //31
M=D //32
@SP //33
M=M+1 //34
//push THAT
@4 //35
A=M //36
D=A //37
@SP //38
A=M //39
M=D //40
@SP //41
M=M+1 //42
//ARG=SP-n-5
@SP //43
D=M //44
@0 //45
D=D-A //46
@5 //47
D=D-A //48
@ARG //49
M=D //50
//LCL=SP
@SP //51
D=M //52
@LCL //53
M=D //54
@Sys.init //55
0;JMP //56
(j_label_0)
//function Main.fibonacci 0
(Main.fibonacci)
//push argument 0
@0 //57
D=A //58
@ARG //59
A=M+D //60
D=M //61
@SP //62
A=M //63
M=D //64
@SP //65
M=M+1 //66
//push constant 2
@2 //67
D=A //68
@SP //69
A=M //70
M=D //71
@SP //72
M=M+1 //73
//lt
@SP //74
M=M-1 //75
A=M //76
D=M //77
@SP //78
M=M-1 //79
A=M //80
A=M //81
D=A-D //82
@j_label_1 //83
D;JLT //84
D=0 //85
@j_label_2 //86
0;JMP //87
(j_label_1)
D=-1 //88
(j_label_2)
@SP //89
A=M //90
M=D //91
@SP //92
M=M+1 //93
//if-goto IF_TRUE
@SP //94
M=M-1 //95
A=M //96
D=M //97
@Main.fibonacci$IF_TRUE //98
D;JNE //99
//goto IF_FALSE
@Main.fibonacci$IF_FALSE //100
0;JMP //101
//label IF_TRUE
(Main.fibonacci$IF_TRUE)
//push argument 0
@0 //102
D=A //103
@ARG //104
A=M+D //105
D=M //106
@SP //107
A=M //108
M=D //109
@SP //110
M=M+1 //111
//return
// R13=FRAME=LCL
@LCL //112
D=M //113
@R13 //114
M=D //115
//RET=*(FRAME-5)
@5 //116
A=D-A //117
D=M //118
@R14 //119
M=D //120
//*ARG=POP()
@SP //121
M=M-1 //122
A=M //123
D=M //124
@ARG //125
A=M //126
M=D //127
//SP=ARG+1
@ARG //128
D=M+1 //129
@SP //130
M=D //131
//THAT=*(FRAME-1)
@R13 //132
M=M-1 //133
A=M //134
D=M //135
@THAT //136
M=D //137
//THIS=*(FRAME-2)
@R13 //138
M=M-1 //139
A=M //140
D=M //141
@THIS //142
M=D //143
//ARG=*(FRAME-3)
@R13 //144
M=M-1 //145
A=M //146
D=M //147
@ARG //148
M=D //149
//LCL=*(FRAME-4)
@R13 //150
M=M-1 //151
A=M //152
D=M //153
@LCL //154
M=D //155
//GOTO RET
@R14 //156
A=M //157
0;JMP //158
//label IF_FALSE
(Main.fibonacci$IF_FALSE)
//push argument 0
@0 //159
D=A //160
@ARG //161
A=M+D //162
D=M //163
@SP //164
A=M //165
M=D //166
@SP //167
M=M+1 //168
//push constant 2
@2 //169
D=A //170
@SP //171
A=M //172
M=D //173
@SP //174
M=M+1 //175
//sub
@SP //176
M=M-1 //177
A=M //178
D=M //179
@SP //180
M=M-1 //181
A=M //182
A=M //183
D=A-D //184
@SP //185
A=M //186
M=D //187
@SP //188
M=M+1 //189
//call Main.fibonacci 1
//push return address
@j_label_5 //190
D=A //191
@SP //192
A=M //193
M=D //194
@SP //195
M=M+1 //196
//push LCL
@1 //197
A=M //198
D=A //199
@SP //200
A=M //201
M=D //202
@SP //203
M=M+1 //204
//push ARG
@2 //205
A=M //206
D=A //207
@SP //208
A=M //209
M=D //210
@SP //211
M=M+1 //212
//push THIS
@3 //213
A=M //214
D=A //215
@SP //216
A=M //217
M=D //218
@SP //219
M=M+1 //220
//push THAT
@4 //221
A=M //222
D=A //223
@SP //224
A=M //225
M=D //226
@SP //227
M=M+1 //228
//ARG=SP-n-5
@SP //229
D=M //230
@1 //231
D=D-A //232
@5 //233
D=D-A //234
@ARG //235
M=D //236
//LCL=SP
@SP //237
D=M //238
@LCL //239
M=D //240
@Main.fibonacci //241
0;JMP //242
(j_label_5)
//push argument 0
@0 //243
D=A //244
@ARG //245
A=M+D //246
D=M //247
@SP //248
A=M //249
M=D //250
@SP //251
M=M+1 //252
//push constant 1
@1 //253
D=A //254
@SP //255
A=M //256
M=D //257
@SP //258
M=M+1 //259
//sub
@SP //260
M=M-1 //261
A=M //262
D=M //263
@SP //264
M=M-1 //265
A=M //266
A=M //267
D=A-D //268
@SP //269
A=M //270
M=D //271
@SP //272
M=M+1 //273
//call Main.fibonacci 1
//push return address
@j_label_8 //274
D=A //275
@SP //276
A=M //277
M=D //278
@SP //279
M=M+1 //280
//push LCL
@1 //281
A=M //282
D=A //283
@SP //284
A=M //285
M=D //286
@SP //287
M=M+1 //288
//push ARG
@2 //289
A=M //290
D=A //291
@SP //292
A=M //293
M=D //294
@SP //295
M=M+1 //296
//push THIS
@3 //297
A=M //298
D=A //299
@SP //300
A=M //301
M=D //302
@SP //303
M=M+1 //304
//push THAT
@4 //305
A=M //306
D=A //307
@SP //308
A=M //309
M=D //310
@SP //311
M=M+1 //312
//ARG=SP-n-5
@SP //313
D=M //314
@1 //315
D=D-A //316
@5 //317
D=D-A //318
@ARG //319
M=D //320
//LCL=SP
@SP //321
D=M //322
@LCL //323
M=D //324
@Main.fibonacci //325
0;JMP //326
(j_label_8)
//add
@SP //327
M=M-1 //328
A=M //329
D=M //330
@SP //331
M=M-1 //332
A=M //333
A=M //334
D=A+D //335
@SP //336
A=M //337
M=D //338
@SP //339
M=M+1 //340
//return
// R13=FRAME=LCL
@LCL //341
D=M //342
@R13 //343
M=D //344
//RET=*(FRAME-5)
@5 //345
A=D-A //346
D=M //347
@R14 //348
M=D //349
//*ARG=POP()
@SP //350
M=M-1 //351
A=M //352
D=M //353
@ARG //354
A=M //355
M=D //356
//SP=ARG+1
@ARG //357
D=M+1 //358
@SP //359
M=D //360
//THAT=*(FRAME-1)
@R13 //361
M=M-1 //362
A=M //363
D=M //364
@THAT //365
M=D //366
//THIS=*(FRAME-2)
@R13 //367
M=M-1 //368
A=M //369
D=M //370
@THIS //371
M=D //372
//ARG=*(FRAME-3)
@R13 //373
M=M-1 //374
A=M //375
D=M //376
@ARG //377
M=D //378
//LCL=*(FRAME-4)
@R13 //379
M=M-1 //380
A=M //381
D=M //382
@LCL //383
M=D //384
//GOTO RET
@R14 //385
A=M //386
0;JMP //387
//function Sys.init 0
(Sys.init)
//push constant 4
@4 //388
D=A //389
@SP //390
A=M //391
M=D //392
@SP //393
M=M+1 //394
//call Main.fibonacci 1
//push return address
@j_label_11 //395
D=A //396
@SP //397
A=M //398
M=D //399
@SP //400
M=M+1 //401
//push LCL
@1 //402
A=M //403
D=A //404
@SP //405
A=M //406
M=D //407
@SP //408
M=M+1 //409
//push ARG
@2 //410
A=M //411
D=A //412
@SP //413
A=M //414
M=D //415
@SP //416
M=M+1 //417
//push THIS
@3 //418
A=M //419
D=A //420
@SP //421
A=M //422
M=D //423
@SP //424
M=M+1 //425
//push THAT
@4 //426
A=M //427
D=A //428
@SP //429
A=M //430
M=D //431
@SP //432
M=M+1 //433
//ARG=SP-n-5
@SP //434
D=M //435
@1 //436
D=D-A //437
@5 //438
D=D-A //439
@ARG //440
M=D //441
//LCL=SP
@SP //442
D=M //443
@LCL //444
M=D //445
@Main.fibonacci //446
0;JMP //447
(j_label_11)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE //448
0;JMP //449
