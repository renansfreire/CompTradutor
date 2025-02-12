class CodeWriter:
    def __init__(self, file_name: str):
        # Open the output file for writing.
        self.file = open(file_name, "w")
        # Store the file name for static label references.
        self.file_name = ""
        # Store the function name for label references.
        self.function_name = "OS"
        # Create a label counter for unique label creation.
        self.label_counter = 0
        # Symbols table for arithmetic operations and assembly symbols.
        self.symbols = {
            # Arithmetic Operators
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or": "M=D|M",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",
            # Assembly Symbols
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "constant": "",
            "static": "",
            "pointer": "@3",
            "temp": "@5"
        }

    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def comment(self, input: str):
        self.write_to_file(["// " + input], False)

    def write_arithmetic(self, command: str):
        output = []
        if command in ["add", "sub", "and", "or"]:
            # Pop Stack into D.
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            # Use the Arithmetic Operator
            output.append(self.symbols[command])
        elif command in ["neg", "not"]:
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["eq", "gt", "lt"]:
            jump_label = "CompLabel" + str(self.label_counter)
            self.label_counter += 1
            # Pop Stack into D.
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            # Calculate the difference
            output.append("D=M-D")
            # Set the Stack to True in anticipation.
            output.append("M=-1")
            # Load the jump label into A.
            output.append("@" + jump_label)
            # Jump if the statement is True.
            # Else update the Stack to False.
            output.append(self.symbols[command])
            # Set the Stack[-1] to False
            output.append("@SP")
            output.append("A=M-1")
            output.append("M=0")
            # Jump label for the True state.
            output.append("(" + jump_label + ")")
        else:
            raise NameError("Unexpected Arithmetic Command")

        # Print assembly commands.
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
                # Put the index value into D.
                output.append("@" + str(index))
                output.append("D=A")
                # Put the base value into A.
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    # Resolve where the segment refers to.
                    output.append(self.symbols[segment])
                    output.append("A=M")
                # Calculate the source address into A.
                output.append("A=D+A")
                # Put the source value into D.
                output.append("D=M")
                # Put D value into where SP points to.
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                # Increment the stack pointer.
                output.append("@SP")
                output.append("M=M+1")
            elif segment == "static":
                # Calculate the source address into A.
                output.append("@" + self.file_name + "." + str(index))
                # Put the source value into D.
                output.append("D=M")
                # Put D value into where SP points to.
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                # Increment the stack pointer.
                output.append("@SP")
                output.append("M=M+1")
            else:
                raise NameError("Unexpected Push Segment")
        elif command == "C_POP":
            if segment == "constant":
                # Not a valid command.
                raise NameError("Cannot Pop Constant Segment")
            elif segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                # Put the index value into D.
                output.append("@" + str(index))
                output.append("D=A")
                # Put the base value into A.
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    # Resolve where the segment refers to.
                    output.append(self.symbols[segment])
                    output.append("A=M")
                # Calculate the source address into D.
                output.append("D=D+A")
                # Put D value into R13 for future use.
                output.append("@R13")
                output.append("M=D")
                # Pop stack value into D.
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                # Put D value into where R13 points to.
                output.append("@R13")
                output.append("A=M")
                output.append("M=D")
            elif segment == "static":
                # Pop stack value into D.
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                # Put the source address into A.
                output.append("@" + self.file_name + "." + str(index))
                # Put D value into static address.
                output.append("M=D")
            else:
                raise NameError("Unexpected Pop Segment")
        else:
            raise NameError("Unexpected Command Type")

        # Print assembly commands.
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
        # Pop stack value into D.
        output.append("@SP")
        output.append("AM=M-1")
        output.append("D=M")
        # Jump to label if D is True
        # (Not Equal to 0)
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
        # Saves the current memory segments and initiates new ones for the called function.
        # return_label is created using the name of the caller function.
        # return_label = file_name.function_name$ret.i
        return_label = self.function_name + "$ret." + str(self.label_counter)
        self.label_counter += 1
        # Output stream is initiated.
        output = []
        # push return_label
        output.append("@" + return_label)
        output.append("D=A")
        output.append("@SP")
        output.append("A=M")
        output.append("M=D")
        output.append("@SP")
        output.append("M=M+1")
        # push LCL, ARG, THIS, and THAT
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            output.append("@" + segment)
            output.append("D=M")
            output.append("@SP")
            output.append("A=M")
            output.append("M=D")
            output.append("@SP")
            output.append("M=M+1")
        # ARG = SP -5 -num_args
        output.append("@SP")
        output.append("D=M")
        output.append("@5")
        output.append("D=D-A")
        output.append("@" + str(num_args))
        output.append("D=D-A")
        output.append("@ARG")
        output.append("M=D")
        # LCL = SP
        output.append("@SP")
        output.append("D=M")
        output.append("@LCL")
        output.append("M=D")
        # goto function_name
        output.append("@" + function_name)
        output.append("0;JMP")
        # (return_label)
        output.append("(" + return_label + ")")
        self.write_to_file(output)

    def write_return(self):
        # Saves the return value and restores the previous call stack.
        # Output stream is initiated.
        output = []
        # frame_end = LCL
        # Store frame_end in R13.
        output.append("@LCL")
        output.append("D=M")
        output.append("@R13")
        output.append("M=D")
        # return_address = *(end_frame -5)
        # Store return address in R14.
        output.append("@5")
        output.append("A=D-A")
        output.append("D=M")
        output.append("@R14")
        output.append("M=D")
        # *ARG = pop()
        output.append("@SP")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@ARG")
        output.append("A=M")
        output.append("M=D")
        # SP = ARG +1
        output.append("@ARG")
        output.append("D=M+1")
        output.append("@SP")
        output.append("M=D")
        # Restore that, this, arg, and lcl segments.
        for segment in ["THAT", "THIS", "ARG", "LCL"]:
            output.append("@R13")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@" + segment)
            output.append("M=D")
        # goto return_address
        output.append("@R14")
        output.append("A=M")
        output.append("0;JMP")
        self.write_to_file(output)

    def write_to_file(self, output: list, new_line=True):
        # Add an empty line for debug purposes.
        if new_line:
            output.append("")
        # Write every line to the output file.
        for line in output:
            print(line, file=self.file)

    def close(self):
        self.file.close()