class IntcodeComputer:
    def __init__(self, mem, i=list(), o=list()):
        self.m = mem
        self.pc = 0
        self.output = o
        self.input = i

    def compute(self, input=[]):
        self.input = input
        for _ in self.run():
            print(self.output)
            pass
        return self.output

    def run(self):
        input = self.input
        class Param:
            def __init__(self, m, addr, mode):
                self.m = m
                self.addr = addr
                self.mode = mode
            
            def get(self):
                if self.mode:
                    return self.m[self.addr]
                else:
                    return self.m[self.m[self.addr]]

            def set(self, v):
                if self.mode:
                    self.m[self.addr] = v
                else:
                    self.m[self.m[self.addr]] = v

        def add(a, b, r):
            r.set(a.get() + b.get())
        
        def mul(a, b, r):
            r.set(a.get() * b.get())

        def inp(a):
            a.set(input.pop(0))

        def outp(a):
            self.output.append(a.get())

        def jnz(a, b):
            if a.get():
                self.pc = b.get()
        
        def jz(a, b):
            if not a.get():
                self.pc = b.get()
        
        def lt(a, b, r):
            r.set(1 if a.get() < b.get() else 0)
        
        def eq(a, b, r):
            r.set(1 if a.get() == b.get() else 0)

        operations = { 1: add, 2: mul, 3: inp, 4: outp, 5: jnz, 6: jz, 7: lt, 8: eq}
        while True:
            pc = self.pc
            instr = self.m[pc]
            o = instr % 100
            if o == 99:
                print(self.m[pc-10:pc+10])
                return
            op = operations[o]
            n = op.__code__.co_argcount
            mode = [ instr//(10**(i+2))%10 for i in range(0, n) ]
            par = [ Param(self.m, pc+1+i, mode[i]) for i in range(0, n)]
            if op == inp and not len(input):
                yield
            op(*par)
            if pc == self.pc:
                self.pc += 1+n