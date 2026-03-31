class Core:
    def __init__(self, lower: float = -1.0, upper: float = 1.0):
        self.lower = lower
        self.upper = upper

    def step(self, x: float, dx: float):
        x_new = x + dx
        if x_new < self.lower or x_new > self.upper:
            return "REJECT", x
        return "ADMISSIBLE", x_new