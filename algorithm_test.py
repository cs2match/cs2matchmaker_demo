import sys

T = int(sys.stdin.readline())
results = []

def fast_adder():
    for _ in range(T):
        A, B = map(int, sys.stdin.readline().split())
        results.append(A + B)
    for res in results:
        print(res)

fast_adder()
