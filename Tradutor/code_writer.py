class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')

    def write_arithmetic(self, command):
        self.file.write(f"// {command}\n")

        if command in ["add", "sub", "and", "or"]:
            op = {"add": "+", "sub": "-", "and": "&", "or": "|"}[command]
            self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M" + op + "D\n")

        elif command in ["neg", "not"]:
            op = {"neg": "-", "not": "!"}[command]
            self.file.write("@SP\nA=M-1\nM=" + op + "M\n")

        elif command in ["eq", "lt", "gt"]:
            jump = {"eq": "JEQ", "lt": "JLT", "gt": "JGT"}[command]
            self.file.write(f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_{self.label_count}
D;{jump}
@SP
A=M-1
M=0
@END_{self.label_count}
0;JMP
(TRUE_{self.label_count})
@SP
A=M-1
M=-1
(END_{self.label_count})
""")
            self.label_count += 1

    def write_push_pop(self, command, segment, index):
        if command == "C_PUSH":
            self.file.write(f"// push {segment} {index}\n")
            if segment == "constant":
                self.file.write(f"@{index}\nD=A\n")
            elif segment in ["local", "argument", "this", "that"]:
                segment_pointer = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"@{segment_pointer}\nD=M\n@{index}\nA=D+A\nD=M\n")
            elif segment == "temp":
                self.file.write(f"@{5 + index}\nD=M\n")
            elif segment == "pointer":
                self.file.write(f"@{'THIS' if index == 0 else 'THAT'}\nD=M\n")
            elif segment == "static":
                self.file.write(f"@Static.{index}\nD=M\n")

            self.file.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif command == "C_POP":
            self.file.write(f"// pop {segment} {index}\n")
            if segment in ["local", "argument", "this", "that"]:
                segment_pointer = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"@{segment_pointer}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n")
            elif segment == "temp":
                self.file.write(f"@{5 + index}\nD=A\n@R13\nM=D\n")
            elif segment == "pointer":
                self.file.write(f"@{'THIS' if index == 0 else 'THAT'}\nD=A\n@R13\nM=D\n")
            elif segment == "static":
                self.file.write(f"@Static.{index}\nD=A\n@R13\nM=D\n")

            self.file.write("@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def close(self):
        self.file.close()
