import random, math, copy


class Solution:

    """
    This class is responsible for a Solution object
    which corresponds to an individual in the population
    """

    def __init__(self, _seq_= None):

        if _seq_ is None:  # If we don't give any sequence information start with an empty list
            self.sequence = list()
        else:
            self.sequence = _seq_
            self.upd()  # Make the necessary updates when you initialize the solution with a given sequence

    def upd(self):

        temp = 0  # tracks time
        rmv = []  # will include the removed orders in the sequence due to redundancy

        redundancy = []
        var = []
        for order in self.sequence:
            if order.id_ not in var:
                var.append(order.id_)
            else:
                redundancy.append(order)

        for order in redundancy:
            self.sequence.remove(order)  # redundancy free area

        for order in self.sequence:
            st = max(order.r, temp)  # starting time of the task
            if st + order.p <= order.d_bar:  # if it is feasible
                order.starting_time = st
                temp = st + order.p
                order.completion_time = temp
                order.tardiness = max(0, order.completion_time - order.d)
            else:
                rmv.append(order)  # if it is not feasible then remove from the sequence

        for order in rmv:
            self.sequence.remove(order)

    def obj(self):

        # Calculates and returns the objective function value of a solution

        return sum([(o.e - o.tardiness*o.w) for o in self.sequence])

    def add_(self, order):

        # Adds the order if the order is not already located in the sequence
        # and then again updates the sequence

        if order not in self.sequence:
            self.sequence.append(order)
            self.upd()

    def w_(self):

        # __str__()

        print([str(o.id_) + '_' for o in self.sequence])


def random_sol(orders):

    # Generates random solution with respect to given orders.
    # It is kind of generator.

    n_seq = random.randint(math.floor(len(orders)/2), len(orders)-1)

    _orders_ = copy.deepcopy(orders)
    rand_orders = []
    count = 0
    while count < n_seq:
        a_ = random.choice(_orders_)
        rand_orders.append(a_)
        _orders_.remove(a_)
        count += 1
    sol = Solution()
    for o in rand_orders:
        sol.add_(o)
    return sol



