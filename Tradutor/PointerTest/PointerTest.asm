// push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@0
M=D
// push constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@1
M=D
// push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2
@SP
AM=M-1
D=M
@2
M=D
// push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 6
@SP
AM=M-1
D=M
@6
M=D
// push pointer 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push pointer 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push this 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push that 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
