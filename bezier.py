import turtle


def interpolate(a, b, factor):
    return a + (b - a) * factor


def vector_interpolate(a, b, factor):
    return interpolate(a[0], b[0], factor), interpolate(a[1], b[1], factor)


def bezier(start, end, p, factor):
    # c1 = vector_interpolate(p, start, factor)
    # c2 = vector_interpolate(c1, end, factor)
    # p = vector_interpolate(c2, c2, factor)
    # return p
    t = factor
    x1 = (1 - t) ** 2 * start.x + 2 * t * (1 - t) * end.x + t ** 2 * p.x
    y1 = (1 - t) ** 2 * start.x + 2 * t * (1 - t) * end.y + t ** 2 * p.y
    p = Point(x1, y1)
    return p


class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    t = turtle.Turtle()
    p1 = Point(0, 0)
    p2 = Point(150, 200)
    p3 = Point(300, -230)
    speed = 100
    while True:
        # t.goto(p3.x, p3.y)
        for i in range(1, speed):
            t_p = i / speed
            p = bezier(p1, p2, p3, t_p)
            t.goto(p.x, p.y)
