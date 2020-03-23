"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # initialize program counter to 0
        self.reg = [0] * 8
        self.ram = [0] * 256
    
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

        HLT = 1
        LDI = 130
        PRN = 71 

        while not halted:

            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                halted = True
                break
            
            elif instruction == LDI:    
                register = operand_a
                integer = operand_b
                self.reg[register] = integer

            elif instruction == PRN:
                register = operand_a
                print(self.reg[register])
            
            self.pc += 1

