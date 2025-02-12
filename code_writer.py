class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.file_name = ""
        self.current_function = ""

    def setFileName(self, file_name):
        self.file_name = file_name.split("/")[-1].split(".")[0]

    def write_arithmetic(self, command):
        if command == "add":
            self.file.write("// add\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n")
        elif command == "sub":
            self.file.write("// sub\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")
        elif command == "neg":
            self.file.write("// neg\n@SP\nA=M-1\nM=-M\n")

    def write_push_pop(self, command, segment, index):
        if command == "C_PUSH":
            self.file.write(f"// push {segment} {index}\n@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif command == "C_POP":
            self.file.write(f"// pop {segment} {index}\n@SP\nAM=M-1\nD=M\n@{index}\nM=D\n")

    def writeLabel(self, label):
        qualified_label = f"({self.current_function}${label})"
        self.file.write(f"// label {label}\n{qualified_label}\n")

    def writeGoto(self, label):
        qualified_label = f"{self.current_function}${label}"
        self.file.write(f"// goto {label}\n@{qualified_label}\n0;JMP\n")

    def writeIf(self, label):
        qualified_label = f"{self.current_function}${label}"
        self.file.write(
            f"// if-goto {label}\n"
            "@SP\nAM=M-1\nD=M\n"
            f"@{qualified_label}\nD;JNE\n"
        )

    def writeFunction(self, function_name, nLocals):
        self.current_function = function_name
        self.file.write(f"// function {function_name} {nLocals}\n({function_name})\n")
        for _ in range(int(nLocals)):
            self.file.write("@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def writeCall(self, function_name, nArgs):
        return_label = f"{self.current_function}$ret.{function_name}"
        self.file.write(
            f"// call {function_name} {nArgs}\n"
            f"@{return_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            f"@{nArgs}\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n"
            "@SP\nD=M\n@LCL\nM=D\n"
            f"@{function_name}\n0;JMP\n"
            f"({return_label})\n"
        )

    def writeReturn(self):
        self.file.write(
            "// return\n"
            "@LCL\nD=M\n@R13\nM=D\n"
            "@5\nA=D-A\nD=M\n@R14\nM=D\n"
            "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
            "@ARG\nD=M+1\n@SP\nM=D\n"
            "@R13\nAM=M-1\nD=M\n@THAT\nM=D\n"
            "@R13\nAM=M-1\nD=M\n@THIS\nM=D\n"
            "@R13\nAM=M-1\nD=M\n@ARG\nM=D\n"
            "@R13\nAM=M-1\nD=M\n@LCL\nM=D\n"
            "@R14\nA=M\n0;JMP\n"
        )

    def close(self):
        self.file.close()
