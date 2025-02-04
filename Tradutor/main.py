import os
import sys
from parser import Parser
from code_writer import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo .vm ou diretório>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".vm")]
        output_file = os.path.join(input_path, os.path.basename(input_path) + ".asm")
    else:
        if not input_path.endswith(".vm"):
            print("Erro: O arquivo de entrada deve ter a extensão .vm")
            sys.exit(1)
        files = [input_path]
        output_file = input_path.replace(".vm", ".asm")
    
    code_writer = CodeWriter(output_file)
    
    for file in files:
        parser = Parser(file)
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            
            if command_type == "C_ARITHMETIC":
                code_writer.write_arithmetic(parser.arg1())
            elif command_type in ["C_PUSH", "C_POP"]:
                code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
    
    code_writer.close()
    print(f"Tradução concluída: {output_file}")

if __name__ == "__main__":
    main()
