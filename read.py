from order import Order


class File(object):

    """
    Responsible with reading a .dat file whose name given
    is given in the constructor.
    """

    def __init__(self, name):

        self.name = name
        datContent = [i.strip().split() for i in open(name).readlines()]

        self.r = [float(x) for x in datContent[1][0][2:-2].split(',')]
        self.p = [float(x) for x in datContent[4][0][2:-2].split(',')]
        self.e = [float(x) for x in datContent[7][0][2:-2].split(',')]
        self.d = [float(x) for x in datContent[10][0][2:-2].split(',')]
        self.d_bar = [float(x) for x in datContent[13][0][2:-2].split(',')]
        self.w = [float(x) for x in datContent[16][0][2:-2].split(',')]

    def get_orders(self):

        # Returns the list of the order objects based on the input data.

        orders = []
        for i in range(len(self.r)):

            orders.append(Order(i, self.r[i], self.p[i], self.e[i], self.d[i], self.d_bar[i], self.w[i]))

        return orders
