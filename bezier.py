import turtle
import math
log=print


class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def log(self):
        log('x is', self.x, 'y is', self.y)


def interpolate(a, b, factor):
    return a + (b - a) * factor


def vector_interpolate(a, b, factor):
    # return interpolate(a[0], b[0], factor), interpolate(a[1], b[1], factor)
    x = interpolate(a.x, b.x, factor)
    y = interpolate(a.y, b.y, factor)
    return Point(x, y)


def bezier2(start, end, p, factor):
    # 上下两个方式都可行
    # 二次线性插值, 二阶贝塞尔
    c1 = vector_interpolate(start, p, factor)
    c2 = vector_interpolate(c1, end, factor)
    p = vector_interpolate(c1, c2, factor)
    # 公式
    # t = factor
    # x1 = (1 - t) ** 2 * start.x + 2 * t * (1 - t) * p.x + t ** 2 * end.x
    # y1 = (1 - t) ** 2 * start.x + 2 * t * (1 - t) * p.y + t ** 2 * end.y
    # p = Point(x1, y1)
    return p


def bezier3(start, end, p1, p2, factor):
    # todo
    # 三阶贝塞尔, 不对呀
    c1 = vector_interpolate(p1, p2, factor)
    c2 = vector_interpolate(start, c1, factor)
    c3 = vector_interpolate(c1, end, factor)
    p = vector_interpolate(c2, c3, factor)
    return p


def bezier_n(factor, *args):
    p = Point(0, 0)
    n = len(args) - 1
    for i in range(0, n + 1):
        pi = args[i]
        c = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        p = p + (c * (factor ** i) * ((1 - factor) ** (n - i))) * pi
    return p


if __name__ == '__main__':
    t = turtle.Turtle()
    p1 = Point(0, 0)
    p2 = Point(150, 200)
    p3 = Point(300, -230)
    p4 = Point(400, 0)
    speed = 20

    # while True:
        # t.goto(p3.x, p3.y)
        # t.goto(p2.x, p2.y)
    for i in range(1, speed):
        t_p = i / speed
        p = bezier_n(t_p, p1, p2, p3, p4)
        # p = bezier3(p1, p2, p3, p4, t_p)
        # p = bezier2(p1, p2, p3, t_p)
        t.goto(p.x, p.y)

    # 画布不消失
    turtle.mainloop()