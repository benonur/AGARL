from solution import *


class Population:

    def __init__(self, pop_size, pool_size, orders=None, solutions=None):

        if solutions is None:
            self.solutions = []
            count = 0
            while count < pop_size:
                self.solutions.append(random_sol(orders))
                count += 1
        else:
            self.solutions = solutions

        self.pop_size = pop_size
        self.pool_size = pool_size

    def _str_(self):

        print([str(s.obj()) for s in self.solutions])

    def form_pool(self):

        pool_sol = []
        count = 0
        while count < self.pool_size:
            sol1 = random.choice(self.solutions)
            sol2 = random.choice(self.solutions)
            which_ = sol1
            if sol2.obj() > sol1.obj():
                which_ = sol2
            pool_sol.append(which_)
            count += 1

        return pool_sol

    def mutation1(self):

        sol1 = random.choice(self.solutions)
        sol2 = random.choice(self.solutions)
        ind1 = random.randint(0, len(sol1.sequence) - 1)
        ind2 = random.randint(0, len(sol2.sequence) - 1)
        ord1 = sol1.sequence[ind1]
        ord2 = sol2.sequence[ind2]

        if ind2 < len(sol1.sequence):
            sol1.sequence[ind2] = ord1
        if ind1 < len(sol2.sequence):
            sol2.sequence[ind1] = ord2
        sol1.upd()
        sol2.upd()

    def mutation2(self):

        sol = random.choice(self.solutions)
        ind1 = random.randint(0, len(sol.sequence) - 1)
        ind2 = random.randint(0, len(sol.sequence) - 1)
        ord1 = sol.sequence[ind1]
        ord2 = sol.sequence[ind2]
        sol.sequence[ind1] = ord2
        sol.sequence[ind2] = ord1
        sol.upd()

    def mutation3(self, orders):

        sol = random.choice(self.solutions)
        ind = random.randint(0, len(sol.sequence) - 1)

        candidates = []
        for o in orders:
            if o not in sol.sequence:
                candidates.append(o)

        order = random.choice(candidates)
        sol.sequence.insert(ind, order)
        sol.upd()

    def best_val(self):

        which_sol, val = None, -1000
        for sol in self.solutions:
            if sol.obj() > val:
                which_sol = sol
                val = sol.obj()

        return which_sol, val

def crossover2(sol1, sol2):

    return sol1, sol2

def crossover(sol1, sol2):

    len1, len2 = len(sol1.sequence), len(sol2.sequence)
    cut_point = random.randint(0, min(len1, len2)-1)
    off1, off2 = list(), list()

    for i, order1 in enumerate(sol1.sequence):
        if i < cut_point:
            off1.append(order1)
        else:
            off2.append(order1)

    for j, order2 in enumerate(sol2.sequence):
        if j < cut_point:
            off2.append(order2)
        else:
            off1.append(order2)

    ins1, ins2 = list(), list()
    real_off1, real_off2 = list(), list()

    for order in off1:
        if order not in real_off1:
            real_off1.append(order)
        else:
            ins2.append(order)

    for order in off2:
        if order not in real_off2:
            real_off2.append(order)
        else:
            ins1.append(order)
    
    sol1 = Solution(_seq_= real_off1)
    sol2 = Solution(_seq_= real_off2)

    for o in ins1:
        which_loc, val = None, sol1.obj()
        for i in range(len(sol1.sequence)):
            _sol1_ = Solution(_seq_=sol1.sequence)
            _sol1_.sequence.insert(i, o)
            if _sol1_.obj() > val:
                which_loc =i
                val = _sol1_.obj()
        if which_loc is None:
            continue
        sol1.sequence.insert(which_loc, o)
        sol1.upd()

    for o in ins2:
        which_loc, val = None, sol2.obj()
        for i in range(len(sol2.sequence)):
            _sol2_ = Solution(_seq_=sol2.sequence)
            _sol2_.sequence.insert(i, o)
            if _sol2_.obj() > val:
                which_loc = i
                val = _sol2_.obj()
        if which_loc is None:
            continue
        sol2.sequence.insert(which_loc, o)
        sol2.upd()

    return sol1, sol2
