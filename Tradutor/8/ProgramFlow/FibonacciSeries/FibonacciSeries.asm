// push argument 1
@1
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@1
D=A
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D

// pop that 0
@0
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D

// pop that 1
@1
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push argument 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D

// sub
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

// pop argument 0
@0
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// label LOOP
(OS$LOOP)

// push argument 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// if-goto COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@OS$COMPUTE_ELEMENT
D;JNE

// goto END
@OS$END
0;JMP

// label COMPUTE_ELEMENT
(OS$COMPUTE_ELEMENT)

// push that 0
@0
D=A
@THAT
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push that 1
@1
D=A
@THAT
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M

// pop that 2
@2
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push pointer 1
@1
D=A
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D

// add
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M

// pop pointer 1
@1
D=A
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push argument 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D

// sub
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

// pop argument 0
@0
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

// goto LOOP
@OS$LOOP
0;JMP

// label END
(OS$END)

