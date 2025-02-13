class CodeWriter:
    def __init__(self, file_name: str):
        self.file = open(file_name, "w")
        self.file_name = ""
        self.function_name = "OS"
        self.label_counter = 0
        self.symbols = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or": "M=D|M",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "constant": "",
            "static": "",
            "pointer": "@3",
            "temp": "@5"
        }
    ##Inclusão do BootStrap
    def writeInit(self):
        output = []
        output.append("@256")
        output.append("D=A")
        output.append("@SP")
        output.append("M=D")
        self.write_to_file(output)
        self.write_function("OS", 0)
        self.write_call("Sys.init", 0)

    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def comment(self, input: str):
        self.write_to_file(["// " + input], False)

    def write_arithmetic(self, command: str):
        output = []
        if command in ["add", "sub", "and", "or"]:
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["neg", "not"]:
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["eq", "gt", "lt"]:
            jump_label = "CompLabel" + str(self.label_counter)
            self.label_counter += 1
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@SP")
            output.append("A=M-1")
            output.append("D=M-D")
            output.append("M=-1")
            output.append("@" + jump_label)
            output.append(self.symbols[command])
            output.append("@SP")
            output.append("A=M-1")
            output.append("M=0")
            output.append("(" + jump_label + ")")
        else:
            raise NameError("Unexpected Arithmetic Command")

        self.write_to_file(output)

    def write_push_pop(self, command: str, segment: str, index: int):
        output = []
        if command == "C_PUSH":
            if segment == "constant":
                output.append("@" + str(index))
                output.append("D=A")
                output.append("@SP")
                output.append("AM=M+1")
                output.append("A=A-1")
                output.append("M=D")
            elif segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                output.append("@" + str(index))
                output.append("D=A")
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    output.append(self.symbols[segment])
                    output.append("A=M")
                output.append("A=D+A")
                output.append("D=M")
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                output.append("@SP")
                output.append("M=M+1")
            elif segment == "static":
                output.append("@" + self.file_name + "." + str(index))
                output.append("D=M")
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                output.append("@SP")
                output.append("M=M+1")
            else:
                raise NameError("Unexpected Push Segment")
        elif command == "C_POP":
            if segment == "constant":
                raise NameError("Cannot Pop Constant Segment")
            elif segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                output.append("@" + str(index))
                output.append("D=A")
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    output.append(self.symbols[segment])
                    output.append("A=M")
                output.append("D=D+A")
                output.append("@R13")
                output.append("M=D")
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                output.append("@R13")
                output.append("A=M")
                output.append("M=D")
            elif segment == "static":

                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                output.append("@" + self.file_name + "." + str(index))

                output.append("M=D")
            else:
                raise NameError("Unexpected Pop Segment")
        else:
            raise NameError("Unexpected Command Type")


        self.write_to_file(output)

    def write_label(self, label: str):
        label_name = self.function_name + "$" + label
        output = []
        output.append("(" + label_name + ")")
        self.write_to_file(output)

    def write_goto(self, label: str):
        label_name = self.function_name + "$" + label
        output = []
        output.append("@" + label_name)
        output.append("0;JMP")
        self.write_to_file(output)

    def write_if(self, label: str):
        label_name = self.function_name + "$" + label
        output = []
        output.append("@SP")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@" + label_name)
        output.append("D;JNE")
        self.write_to_file(output)

    def write_function(self, function_name: str, num_vars: int):
        output = []
        self.function_name = function_name
        output.append("(" + self.function_name + ")")
        self.write_to_file(output)
        for _ in range(num_vars):
            self.write_push_pop("C_PUSH", "constant", 0)

    def write_call(self, function_name: str, num_args: int):
        
        return_label = self.function_name + "$ret." + str(self.label_counter)
        self.label_counter += 1
        output = []
        output.append("@" + return_label)
        output.append("D=A")
        output.append("@SP")
        output.append("A=M")
        output.append("M=D")
        output.append("@SP")
        output.append("M=M+1")
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            output.append("@" + segment)
            output.append("D=M")
            output.append("@SP")
            output.append("A=M")
            output.append("M=D")
            output.append("@SP")
            output.append("M=M+1")
        output.append("@SP")
        output.append("D=M")
        output.append("@5")
        output.append("D=D-A")
        output.append("@" + str(num_args))
        output.append("D=D-A")
        output.append("@ARG")
        output.append("M=D")
        output.append("@SP")
        output.append("D=M")
        output.append("@LCL")
        output.append("M=D")
        output.append("@" + function_name)
        output.append("0;JMP")
        output.append("(" + return_label + ")")
        self.write_to_file(output)

    def write_return(self):

        output = []
        output.append("@LCL")
        output.append("D=M")
        output.append("@R13")
        output.append("M=D")
        output.append("@5")
        output.append("A=D-A")
        output.append("D=M")
        output.append("@R14")
        output.append("M=D")
        output.append("@SP")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@ARG")
        output.append("A=M")
        output.append("M=D")
        output.append("@ARG")
        output.append("D=M+1")
        output.append("@SP")
        output.append("M=D")
        for segment in ["THAT", "THIS", "ARG", "LCL"]:
            output.append("@R13")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@" + segment)
            output.append("M=D")
        output.append("@R14")
        output.append("A=M")
        output.append("0;JMP")
        self.write_to_file(output)

    def write_to_file(self, output: list, new_line=True):
        if new_line:
            output.append("")
        for line in output:
            print(line, file=self.file)

    def close(self):
        self.file.close()