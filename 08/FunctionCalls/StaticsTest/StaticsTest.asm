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
//function Class1.set 0
(Class1.set)
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
//pop static 0
@Class1.0 //67
D=A //68
@R13 //69
M=D //70
@SP //71
M=M-1 //72
A=M //73
D=M //74
@R13 //75
A=M //76
M=D //77
//push argument 1
@1 //78
D=A //79
@ARG //80
A=M+D //81
D=M //82
@SP //83
A=M //84
M=D //85
@SP //86
M=M+1 //87
//pop static 1
@Class1.1 //88
D=A //89
@R13 //90
M=D //91
@SP //92
M=M-1 //93
A=M //94
D=M //95
@R13 //96
A=M //97
M=D //98
//push constant 0
@0 //99
D=A //100
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
//function Class1.get 0
(Class1.get)
//push static 0
@Class1.0 //153
D=M //154
@SP //155
A=M //156
M=D //157
@SP //158
M=M+1 //159
//push static 1
@Class1.1 //160
D=M //161
@SP //162
A=M //163
M=D //164
@SP //165
M=M+1 //166
//sub
@SP //167
M=M-1 //168
A=M //169
D=M //170
@SP //171
M=M-1 //172
A=M //173
A=M //174
D=A-D //175
@SP //176
A=M //177
M=D //178
@SP //179
M=M+1 //180
//return
// R13=FRAME=LCL
@LCL //181
D=M //182
@R13 //183
M=D //184
//RET=*(FRAME-5)
@5 //185
A=D-A //186
D=M //187
@R14 //188
M=D //189
//*ARG=POP()
@SP //190
M=M-1 //191
A=M //192
D=M //193
@ARG //194
A=M //195
M=D //196
//SP=ARG+1
@ARG //197
D=M+1 //198
@SP //199
M=D //200
//THAT=*(FRAME-1)
@R13 //201
M=M-1 //202
A=M //203
D=M //204
@THAT //205
M=D //206
//THIS=*(FRAME-2)
@R13 //207
M=M-1 //208
A=M //209
D=M //210
@THIS //211
M=D //212
//ARG=*(FRAME-3)
@R13 //213
M=M-1 //214
A=M //215
D=M //216
@ARG //217
M=D //218
//LCL=*(FRAME-4)
@R13 //219
M=M-1 //220
A=M //221
D=M //222
@LCL //223
M=D //224
//GOTO RET
@R14 //225
A=M //226
0;JMP //227
//function Class2.set 0
(Class2.set)
//push argument 0
@0 //228
D=A //229
@ARG //230
A=M+D //231
D=M //232
@SP //233
A=M //234
M=D //235
@SP //236
M=M+1 //237
//pop static 0
@Class2.0 //238
D=A //239
@R13 //240
M=D //241
@SP //242
M=M-1 //243
A=M //244
D=M //245
@R13 //246
A=M //247
M=D //248
//push argument 1
@1 //249
D=A //250
@ARG //251
A=M+D //252
D=M //253
@SP //254
A=M //255
M=D //256
@SP //257
M=M+1 //258
//pop static 1
@Class2.1 //259
D=A //260
@R13 //261
M=D //262
@SP //263
M=M-1 //264
A=M //265
D=M //266
@R13 //267
A=M //268
M=D //269
//push constant 0
@0 //270
D=A //271
@SP //272
A=M //273
M=D //274
@SP //275
M=M+1 //276
//return
// R13=FRAME=LCL
@LCL //277
D=M //278
@R13 //279
M=D //280
//RET=*(FRAME-5)
@5 //281
A=D-A //282
D=M //283
@R14 //284
M=D //285
//*ARG=POP()
@SP //286
M=M-1 //287
A=M //288
D=M //289
@ARG //290
A=M //291
M=D //292
//SP=ARG+1
@ARG //293
D=M+1 //294
@SP //295
M=D //296
//THAT=*(FRAME-1)
@R13 //297
M=M-1 //298
A=M //299
D=M //300
@THAT //301
M=D //302
//THIS=*(FRAME-2)
@R13 //303
M=M-1 //304
A=M //305
D=M //306
@THIS //307
M=D //308
//ARG=*(FRAME-3)
@R13 //309
M=M-1 //310
A=M //311
D=M //312
@ARG //313
M=D //314
//LCL=*(FRAME-4)
@R13 //315
M=M-1 //316
A=M //317
D=M //318
@LCL //319
M=D //320
//GOTO RET
@R14 //321
A=M //322
0;JMP //323
//function Class2.get 0
(Class2.get)
//push static 0
@Class2.0 //324
D=M //325
@SP //326
A=M //327
M=D //328
@SP //329
M=M+1 //330
//push static 1
@Class2.1 //331
D=M //332
@SP //333
A=M //334
M=D //335
@SP //336
M=M+1 //337
//sub
@SP //338
M=M-1 //339
A=M //340
D=M //341
@SP //342
M=M-1 //343
A=M //344
A=M //345
D=A-D //346
@SP //347
A=M //348
M=D //349
@SP //350
M=M+1 //351
//return
// R13=FRAME=LCL
@LCL //352
D=M //353
@R13 //354
M=D //355
//RET=*(FRAME-5)
@5 //356
A=D-A //357
D=M //358
@R14 //359
M=D //360
//*ARG=POP()
@SP //361
M=M-1 //362
A=M //363
D=M //364
@ARG //365
A=M //366
M=D //367
//SP=ARG+1
@ARG //368
D=M+1 //369
@SP //370
M=D //371
//THAT=*(FRAME-1)
@R13 //372
M=M-1 //373
A=M //374
D=M //375
@THAT //376
M=D //377
//THIS=*(FRAME-2)
@R13 //378
M=M-1 //379
A=M //380
D=M //381
@THIS //382
M=D //383
//ARG=*(FRAME-3)
@R13 //384
M=M-1 //385
A=M //386
D=M //387
@ARG //388
M=D //389
//LCL=*(FRAME-4)
@R13 //390
M=M-1 //391
A=M //392
D=M //393
@LCL //394
M=D //395
//GOTO RET
@R14 //396
A=M //397
0;JMP //398
//function Sys.init 0
(Sys.init)
//push constant 6
@6 //399
D=A //400
@SP //401
A=M //402
M=D //403
@SP //404
M=M+1 //405
//push constant 8
@8 //406
D=A //407
@SP //408
A=M //409
M=D //410
@SP //411
M=M+1 //412
//call Class1.set 2
//push return address
@j_label_5 //413
D=A //414
@SP //415
A=M //416
M=D //417
@SP //418
M=M+1 //419
//push LCL
@1 //420
A=M //421
D=A //422
@SP //423
A=M //424
M=D //425
@SP //426
M=M+1 //427
//push ARG
@2 //428
A=M //429
D=A //430
@SP //431
A=M //432
M=D //433
@SP //434
M=M+1 //435
//push THIS
@3 //436
A=M //437
D=A //438
@SP //439
A=M //440
M=D //441
@SP //442
M=M+1 //443
//push THAT
@4 //444
A=M //445
D=A //446
@SP //447
A=M //448
M=D //449
@SP //450
M=M+1 //451
//ARG=SP-n-5
@SP //452
D=M //453
@2 //454
D=D-A //455
@5 //456
D=D-A //457
@ARG //458
M=D //459
//LCL=SP
@SP //460
D=M //461
@LCL //462
M=D //463
@Class1.set //464
0;JMP //465
(j_label_5)
//pop temp 0
@0 //466
D=A //467
@5 //468
D=A+D //469
@R13 //470
M=D //471
@SP //472
M=M-1 //473
A=M //474
D=M //475
@R13 //476
A=M //477
M=D //478
//push constant 23
@23 //479
D=A //480
@SP //481
A=M //482
M=D //483
@SP //484
M=M+1 //485
//push constant 15
@15 //486
D=A //487
@SP //488
A=M //489
M=D //490
@SP //491
M=M+1 //492
//call Class2.set 2
//push return address
@j_label_6 //493
D=A //494
@SP //495
A=M //496
M=D //497
@SP //498
M=M+1 //499
//push LCL
@1 //500
A=M //501
D=A //502
@SP //503
A=M //504
M=D //505
@SP //506
M=M+1 //507
//push ARG
@2 //508
A=M //509
D=A //510
@SP //511
A=M //512
M=D //513
@SP //514
M=M+1 //515
//push THIS
@3 //516
A=M //517
D=A //518
@SP //519
A=M //520
M=D //521
@SP //522
M=M+1 //523
//push THAT
@4 //524
A=M //525
D=A //526
@SP //527
A=M //528
M=D //529
@SP //530
M=M+1 //531
//ARG=SP-n-5
@SP //532
D=M //533
@2 //534
D=D-A //535
@5 //536
D=D-A //537
@ARG //538
M=D //539
//LCL=SP
@SP //540
D=M //541
@LCL //542
M=D //543
@Class2.set //544
0;JMP //545
(j_label_6)
//pop temp 0
@0 //546
D=A //547
@5 //548
D=A+D //549
@R13 //550
M=D //551
@SP //552
M=M-1 //553
A=M //554
D=M //555
@R13 //556
A=M //557
M=D //558
//call Class1.get 0
//push return address
@j_label_7 //559
D=A //560
@SP //561
A=M //562
M=D //563
@SP //564
M=M+1 //565
//push LCL
@1 //566
A=M //567
D=A //568
@SP //569
A=M //570
M=D //571
@SP //572
M=M+1 //573
//push ARG
@2 //574
A=M //575
D=A //576
@SP //577
A=M //578
M=D //579
@SP //580
M=M+1 //581
//push THIS
@3 //582
A=M //583
D=A //584
@SP //585
A=M //586
M=D //587
@SP //588
M=M+1 //589
//push THAT
@4 //590
A=M //591
D=A //592
@SP //593
A=M //594
M=D //595
@SP //596
M=M+1 //597
//ARG=SP-n-5
@SP //598
D=M //599
@0 //600
D=D-A //601
@5 //602
D=D-A //603
@ARG //604
M=D //605
//LCL=SP
@SP //606
D=M //607
@LCL //608
M=D //609
@Class1.get //610
0;JMP //611
(j_label_7)
//call Class2.get 0
//push return address
@j_label_8 //612
D=A //613
@SP //614
A=M //615
M=D //616
@SP //617
M=M+1 //618
//push LCL
@1 //619
A=M //620
D=A //621
@SP //622
A=M //623
M=D //624
@SP //625
M=M+1 //626
//push ARG
@2 //627
A=M //628
D=A //629
@SP //630
A=M //631
M=D //632
@SP //633
M=M+1 //634
//push THIS
@3 //635
A=M //636
D=A //637
@SP //638
A=M //639
M=D //640
@SP //641
M=M+1 //642
//push THAT
@4 //643
A=M //644
D=A //645
@SP //646
A=M //647
M=D //648
@SP //649
M=M+1 //650
//ARG=SP-n-5
@SP //651
D=M //652
@0 //653
D=D-A //654
@5 //655
D=D-A //656
@ARG //657
M=D //658
//LCL=SP
@SP //659
D=M //660
@LCL //661
M=D //662
@Class2.get //663
0;JMP //664
(j_label_8)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE //665
0;JMP //666
