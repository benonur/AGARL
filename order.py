class Order:

    def __init__(self,i, r, p, e, d, d_bar, w):

        self.id_ = i
        self.r = r
        self.p = p
        self.e = e
        self.d = d
        self.d_bar = d_bar
        self.w = w

        self.starting_time = None
        self.completion_time = None
        self.tardiness = None

