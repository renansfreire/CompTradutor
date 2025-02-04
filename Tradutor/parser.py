class Parser:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.lines = [line.split("//")[0].strip() for line in f.readlines() if line.strip() and not line.startswith("//")]
        self.current_command = None
        self.index = -1

    def has_more_commands(self):
        return self.index < len(self.lines) - 1

    def advance(self):
        if self.has_more_commands():
            self.index += 1
            self.current_command = self.lines[self.index]

    def command_type(self):
        if not self.current_command:
            return None
        if self.current_command.startswith("push"):
            return "C_PUSH"
        elif self.current_command.startswith("pop"):
            return "C_POP"
        else:
            return "C_ARITHMETIC"

    def arg1(self):
        if not self.current_command:
            return None
        return self.current_command.split()[1] if self.command_type() != "C_ARITHMETIC" else self.current_command.split()[0]

    def arg2(self):
        if not self.current_command or self.command_type() not in ["C_PUSH", "C_POP"]:
            return None
        return int(self.current_command.split()[2])
