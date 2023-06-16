# class Parabola fits a parabola given three x,y pairs
class Parabola:
    def __init__(self, p1,p2,p3):
        x = [p1[0], p2[0], p3[0]]
        y = [p1[1], p2[1], p3[1]]
        self.a = y[0] / ((x[0] - x[1]) * (x[0] - x[2]))
        self.a += y[1] / ((x[1] - x[0]) * (x[1] - x[2]))
        self.a += y[2] / ((x[2] - x[0]) * (x[2] - x[1]))
        self.b = -(x[1] + x[2]) * y[0] / ((x[0] - x[1]) * (x[0] - x[2]))
        self.b -= (x[0] + x[2]) * y[1] / ((x[1] - x[0]) * (x[1] - x[2]))
        self.b -= (x[0] + x[1]) * y[2] / ((x[2] - x[0]) * (x[2] - x[1]))
        self.c = x[1] * x[2] * y[0] / ((x[0] - x[1]) * (x[0] - x[2]))
        self.c += x[0] * x[2] * y[1] / ((x[1] - x[0]) * (x[1] - x[2]))
        self.c += x[0] * x[1] * y[2] / ((x[2] - x[0]) * (x[2] - x[1]))

    def eval(self, x: int):
        return self.a*x*x+self.b*x+self.c
