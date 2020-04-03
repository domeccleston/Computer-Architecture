# Inventory

- ls8.py: Import and instantiate CPU from cpu.py. Call `load()` and `run()`.

- cpu.py: 
    - Not fully implemented yet: missing constructor and `run()`.
    - `load()`: currently has a program (list of binary numbers) hardcoded. Iterate through this list and load each into `self.ram`.
    - `alu()`: handles Arithmetics and Logic Operations. Currently this just deals with 'ADD', by incrementing register a by register b.
    - `trace()`: prints CPU state for debugging
    - Missing at least attributes `self.ram, self.pc, self.fl, self.ie, self.reg` and method `self.ram_read` 

- /examples:
    - List of binary .ls8 programs for the LS8 computer to run
    
     