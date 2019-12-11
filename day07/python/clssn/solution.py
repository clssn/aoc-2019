import computer
import itertools

def amplify(phase_set, code, inp=0):
    for p in phase_set:
        i=[p, inp]
        c = computer.IntcodeComputer(list(code))
        output = c.compute(i)
        inp = output[-1]
    return inp

def amplify_fb(phase_set, code, inp=0):
    s = len(phase_set)
    fifos = [ [p] for p in phase_set ]
    fifos[0].append(inp)
    amplifiers = [ computer.IntcodeComputer(list(code), fifos[i], fifos[(i+1)%s]) for i in range(s) ]
    runners = [ (amp, amp.run()) for amp in amplifiers ]
    while True:
        try:
            for r in runners:
                amp, runner = r
                next(runner)
        except StopIteration:
            print(amp.output)
            return amp.output[-1]

def brute(code, feedback):
    perms = itertools.permutations(range(5, 10)) if feedback else itertools.permutations(range(5))
    fn = amplify_fb if feedback else amplify
    results = set([(phase_set, fn(phase_set, list(code))) for phase_set in perms])
    m = max(results, key=lambda a: a[1])
    return m
    

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [ int(x) for x in f.readline().split(',') ]
    print("Solution star1: {}".format(brute(list(code), feedback=False)))
    print("Solution star2: {}".format(brute(list(code), feedback=True)))

