# Inspired from my personal utils file for AoC

from collections import deque
from functools import reduce
import heapq
from typing import List, Tuple, Dict, Any


# Strings, lists
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str) -> List[int]:
    return lmap(int, s.split())


def words(s: str) -> List[str]:
    return s.split()


# Algorithms
def binary_search(f, lo=0, hi=None):
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo + offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far


def bfs(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    visited = set()
    queue = deque([start])
    result = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            queue.extend(graph.get(node, []))
    return result


def a_star(start, goal, neighbors, h):
    pq = [(h(start), 0, start, [start])]
    visited = set()
    while pq:
        f_score, g_score, current, path = heapq.heappop(pq)
        if current == goal:
            return path, g_score
        if current in visited:
            continue
        visited.add(current)
        for neighbor, cost in neighbors(current):
            if neighbor in visited:
                continue
            new_g_score = g_score + cost
            new_path = path + [neighbor]
            heapq.heappush(pq, (new_g_score + h(neighbor),
                           new_g_score, neighbor, new_path))
    return None, float('inf')


# Maths
def isPrime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def allPrimesToX(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(limit**0.5) + 1):
        if sieve[start]:
            for multiple in range(start * start, limit + 1, start):
                sieve[multiple] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime]


# Data structures
class UnionFind:
    def __init__(self, n: int):
        self.n = n
        self.parents = [None] * n
        self.ranks = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        p = self.parents[i]
        if p is None:
            return i
        p = self.find(p)
        self.parents[i] = p
        return p

    def in_same_set(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)

    def merge(self, i: int, j: int) -> None:
        i = self.find(i)
        j = self.find(j)
        if i == j:
            return
        if self.ranks[i] < self.ranks[j]:
            self.parents[i] = j
        elif self.ranks[i] > self.ranks[j]:
            self.parents[j] = i
        else:
            self.parents[j] = i
            self.ranks[i] += 1
        self.num_sets -= 1


class Linked:
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, value):
        new_node = Linked(value)
        current = self
        while current.next:
            current = current.next
        current.next = new_node


# List/Vector operations
DIRS4 = [[-1, 0], [1, 0], [0, -1], [0, 1]]
DIRS8 = DIRS4 + [[-1, -1], [-1, 1], [1, -1], [1, 1]]


def padd(x, y):
    return [a + b for a, b in zip(x, y)]


def pneg(v):
    return [-i for i in v]


def psub(x, y):
    return [a - b for a, b in zip(x, y)]


def pdist1(x, y=None):
    if y is not None:
        x = psub(x, y)
    return sum(map(abs, x))


# Matrices
def matmat(a, b):
    n, k1 = len(a), len(a[0])
    k2, m = len(b), len(b[0])
    assert k1 == k2
    return [[sum(a[i][k] * b[k][j] for k in range(k1)) for j in range(m)] for i in range(n)]


def matvec(a, v):
    return [j for i in matmat(a, [[x] for x in v]) for j in i]


def matexp(a, k):
    n = len(a)
    out = [[int(i == j) for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            out = matmat(a, out)
        a = matmat(a, a)
        k //= 2
    return out


# Miscellaneous
def manhattan(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    return sum(abs(a - b) for a, b in zip(point1, point2))


def bounds(a, b, limit):
    return 0 <= a < limit and 0 <= b < limit


def lcmWithRemainder(a: List[int], n: List[int]) -> int:
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        return gcd, y1, x1 - (a // b) * y1

    def mod_inverse(a, m):
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return x % m

    if len(a) != len(n):
        raise ValueError("Lists 'a' and 'n' must have the same length.")
    if all(rem == 0 for rem in a):
        return 0
    N = reduce(lambda x, y: x * y, n)
    result = 0
    for ai, ni in zip(a, n):
        Ni = N // ni
        Mi = mod_inverse(Ni, ni)
        result += ai * Ni * Mi
    return result % N
