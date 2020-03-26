"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # initialize program counter to 0
        self.reg = [0] * 8
        self.ram = [0] * 256

        # system stack
        self.SP = 7
        self.reg[self.SP] = 0xf4

        self.instructions = {
            1: "HLT",
            130: "LDI",
            71: "PRN",
            162: "MUL"
        }

        self.branch_table = {
            1: self.halt,
            130: self.load_immediate,
            71: self._print,
            162: self.mult,
            69: self.push,
            70: self.pop,
            80: self.call,
        }
    
    def call(self, instruction, operand_a, operand_b):
        reg = self.ram[self.pc + 1]
        
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc + 2

        self.pc = self.reg[reg]

    def ret(self, instruction, operand_a, operand_b):
        self.pc = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1


    def push(self, instruction, operand_a, operand_b):
        self.reg[self.SP] -= 1
        reg_num = self.ram[self.pc + 1]
        reg_val = self.reg[reg_num]
        self.ram[self.reg[self.SP]] = reg_val
        self.pc += 2

    def pop(self, instruction, operand_a, operand_b):
        reg_num = self.ram[self.pc + 1]
        popped_value = self.ram[self.reg[self.SP]]
        self.reg[reg_num] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc += 2
        return popped_value

    def halt(self, instruction, operand_a, operand_b):
        halted = True
        sys.exit(1)

    def load_immediate(self, instruction, operand_a, operand_b):
        register = operand_a
        integer = operand_b
        self.reg[register] = integer
        self.pc += 3

    def _print(self, instruction, operand_a, operand_b):
        register = operand_a
        print(self.reg[register])
        self.pc += 1

    def mult(self, instruction, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3
    
    def ram_read(self, address):
        return self.ram[address]

    def raw_write(self, address, value):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        address = 0

        program_list = []

        with open(program, "r") as program_file:
            for line in program_file:
                line = line.partition('#')[0]
                line = line.rstrip()
                if line:
                    program_list.append(int(line, 2))


        for instruction in program_list:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):  
        """Run the CPU."""

        halted = False
        
        while not halted:

            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # execute the instruction
            if instruction in self.branch_table:
                self.branch_table[instruction](instruction, operand_a, operand_b)
            else:
                self.pc += 1

