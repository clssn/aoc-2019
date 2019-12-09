import computer
import itertools

def amplify(phase_sets, code, inp=0):
    for p in phase_sets:
        i=[p, inp]
        c = computer.IntcodeComputer(list(code))
        output = c.compute(i)
        inp = output[-1]
    return inp

def brute(code):
    perms = itertools.permutations(range(5))
    results = set([(phase_sets, amplify(phase_sets, list(code))) for phase_sets in perms])
    m =max(results, key=lambda a: a[1])
    return m
    

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [ int(x) for x in f.readline().split(',') ]
    print("Solution star1: {}".format(brute(code)))

