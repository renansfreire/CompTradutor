import os
import sys
from parser import Parser
from code_writerBS import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Error: No input file is found.")
        print("Usage: python " + __file__ + " [file.vm] | [directory]")
        return

    input_files = []
    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".vm"):
        input_files.append(input_path)
        output_file_name = os.path.join(os.path.dirname(input_path), os.path.basename(input_path)[:-3] + ".asm")
  
    elif os.path.isdir(input_path):
        if input_path.endswith("/"):
            input_path = input_path[:-1]
        for file_name in os.listdir(input_path):
            if file_name.endswith(".vm"):
                input_files.append(os.path.join(input_path, file_name))
        if len(input_files) == 0:
            raise NameError("No Input File Found")
        output_file_name = os.path.join(input_path, os.path.basename(input_path) + ".asm")
    else:
        raise NameError("Unknown Input Path")

    code_writer = CodeWriter(output_file_name)
    ##Inclusão do BootStrap
    code_writer.comment("Bootstrap Code")
    code_writer.writeInit()

    for input_file_name in input_files:
        file_name = os.path.basename(input_file_name).replace(".vm", "")
        code_writer.set_file_name(file_name)

        parser = Parser(input_file_name)

        while parser.hasMoreCommands():
            parser.advance()
            code_writer.comment(parser.current_command)
            command_type = parser.commandType()
            if command_type == "C_ARITHMETIC":
                code_writer.write_arithmetic(parser.arg1())
            elif command_type in ["C_PUSH", "C_POP"]:
                segment = parser.arg1()
                index = parser.arg2()
                code_writer.write_push_pop(command_type, segment, index)
            elif command_type == "C_LABEL":
                code_writer.write_label(parser.arg1())
            elif command_type == "C_GOTO":
                code_writer.write_goto(parser.arg1())
            elif command_type == "C_IF":
                code_writer.write_if(parser.arg1())
            elif command_type == "C_FUNCTION":
                function_name = parser.arg1()
                num_vars = parser.arg2()
                code_writer.write_function(function_name, num_vars)
            elif command_type == "C_CALL":
                function_name = parser.arg1()
                num_args = parser.arg2()
                code_writer.write_call(function_name, num_args)
            elif command_type == "C_RETURN":
                code_writer.write_return()
            else:
                raise NameError("Unsupported Command Type")

    code_writer.close()

if __name__ == "__main__":
    main()