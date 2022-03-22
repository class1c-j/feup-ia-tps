#!/usr/bin/env python3

"""

State representation:
States are represented by (A, B) where A in [0..4], B in [0..3].

Starting state:
(0, 0)

Operators:





PourBAFull -> pours B into A until A is full.
Preconditions -> B > 0 and A < 4 and B >= 4 - A
Effects -> B = B - (4 - A); A = 4
Cost = 1

PourABEmpty -> pours A into B until A is empty.
Preconditions -> A > 0 and B < 3 and A < 3 - B
Effects -> A = 0; B = B + A
Cost -> 1

PourBAEmpty -> pours B into A until B is empty.
Preconditions -> B > 0 and A < 4 and B < 4 - A
Effects -> B = 0; A = A + B
Cost -> 1

Objective Test:
State is in the form (n, _).

"""

max_a, max_b = 4, 3

def is_objective_state(state):
    return state.bucket_a == 2

objective_function = is_objective_state

class BucketsState:
    def __init__(self, capacities, previous=None):
        self.bucket_a, self.bucket_b = capacities
        self.previous = previous

    def __eq__(self, other):
        return self.bucket_a == other.bucket_a and self.bucket_b == other.bucket_b

    def __repr__(self):
        return f'({self.bucket_a}, {self.bucket_b})'

"""
FillA -> fills bucket A.
Preconditions -> A < 4
Effects -> A = 4; B = B
Cost -> 1
"""
def fillA(state):
    if state.bucket_a >= max_a:
        return
    return BucketsState((max_a, state.bucket_b))

"""
FillB -> fills bucket B.
Preconditions -> B < 3
Effects -> A = A; B = 3
Cost -> 1
"""
def fillB(state):
    if state.bucket_b >= max_b:
        return
    return BucketsState((state.bucket_a, max_b))

"""
EmptyA -> empties bucket A.
Preconditions -> A > 0
Effects -> A = 0
Cost -> 1
"""
def emptyA(state):
    if state.bucket_a <= 0:
        return
    return BucketsState((0, state.bucket_b))

"""
EmptyB -> empties bucket B.
Preconditions -> B > 0
Effects -> B = 0
Cost -> 1
"""
def emptyB(state):
    if state.bucket_b <= 0:
        return
    return BucketsState((state.bucket_a, 0))

"""
PourABFull -> pours A into B until B is full.
Preconditions -> A > 0 and B < 3 and A >= 3 - B
Effects -> A = A - (3 - B); B = 3
Cost = 1
"""
def pourABFull(state):
    if state.bucket_b >= max_b or state.bucket_a < max_b - state.bucket_b:
        return
    return BucketsState((state.bucket_a - (max_b - state.bucket_b), max_b))

def pourBAFull(state):
    if state.bucket_a >= max_a or state.bucket_b < max_a - state.bucket_a:
        return
    return BucketsState((max_a, state.bucket_b - (max_a - state.bucket_a)))

def pourABEmpty(state):
    if state.bucket_b >= max_b or state.bucket_a >= max_b - state.bucket_b:
        return
    return BucketsState((0, state.bucket_a + state.bucket_b))

def pourBAEmpty(state):
    if state.bucket_a >= max_a or state.bucket_b >= max_a - state.bucket_a:
        return
    return BucketsState((state.bucket_a + state.bucket_b, 0))

operators = [fillA, fillB, emptyA, emptyB, pourABFull, pourBAFull, pourABEmpty, pourBAEmpty]

def bfs(start):
    queue = [start]
    visited = []

    while queue:
        current = queue.pop(0)
        if (current.bucket_a, current.bucket_b) in visited:
            continue
        if objective_function(current):
            solution = current
            break
        for op in operators:
            next = op(current)
            if not next:
                continue
            next.previous = current
            visited.append((current.bucket_a, current.bucket_b))
            queue.append(next)

    path = []
    while solution:
        path.append(solution)
        solution = solution.previous

    return list(reversed(path))

print("Solution", bfs(BucketsState((0, 0))))
