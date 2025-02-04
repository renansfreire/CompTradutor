class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')

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

    def close(self):
        self.file.close()
