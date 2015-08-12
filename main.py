from __future__ import division

import turtle
import math
import random
import json


__author__ = 'gua'


# =====
# config
# =====

pattern_path = 'pattern.json'
# pattern_path = 'heart.json'

# line_length
line_length = 120
bezier_steps = 60

# setup colors
black = (0, 0, 0)
magenta = (1, 0, 0.7)
colors = []
for n in range(20):
    color_split = random.randint(30, 60)
    for i in range(70):
        if i < color_split:
            colors.append(black)
        else:
            colors.append(magenta)

color_index = 0


# =====
# math
# =====

def vector_length(v):
    x, y = v
    return math.sqrt(x * x + y * y)


def interpolate(a, b, factor):
    return a + (b - a) * factor


def vector_interpolate(a, b, factor):
    return interpolate(a[0], b[0], factor), interpolate(a[1], b[1], factor)


def bezier(start, end, p1, p2, factor):
    c1 = vector_interpolate(p1, p2, factor)
    c2 = vector_interpolate(start, c1, factor)
    c3 = vector_interpolate(c1, end, factor)
    p = vector_interpolate(c2, c3, factor)
    return p


def draw_sketch_line(pen, a, b, noise=1, steps=5):
    t = pen
    t.penup()
    t.goto(*a)
    t.pendown()

    v_length = vector_length((a[0] - b[0], a[1] - b[1]))
    steps = int(min(steps, v_length / 10))
    points = []
    for i in xrange(steps):
        x, y = vector_interpolate(a, b, i / steps)
        offset = random.randint(-noise, noise)
        x = x + offset
        y = y + offset
        points.append((x, y))
    points.append(b)

    for p in points:
        t.goto(*p)
    t.goto(a)


def draw_step(pen, color, x, y, factor):
    t = pen

    t.left(90)
    mid = 0.5
    length = (mid - abs(factor - mid)) * line_length
    t.pencolor(*color)

    # get line positions
    current_position = t.position()
    t.penup()
    t.fd(length)
    position_b = t.position()
    t.back(length)
    t.pendown()
    t.right(90)

    draw_sketch_line(t, current_position, position_b)
    # t.goto(position_b)
    # t.goto(position_a)

    rotation = t.towards(x, y)
    t.right(t.heading() - rotation)

    # move to next point
    distance = t.distance(x, y)
    t.penup()
    t.forward(distance)
    t.pendown()


def draw_bezier(pen, steps, start, end, p1, p2):
    points = []
    for i in range(steps):
        t = i / (steps - 1)

        global color_index
        color = colors[color_index]
        color_index += 1

        pos = bezier(start, end, p1, p2, t)
        points.append(pos)
        draw_step(pen, color, pos[0], pos[1], i / steps)
    return points


def draw_pattern(pattern):
    n = len(pattern) // 4
    for i in range(n):
        s, e = i * 4, i * 4 + 4
        start, end, p1, p2 = pattern[s:e]
        draw_bezier(t, bezier_steps, start, end, p1, p2)
        turtle.update()


def load(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


def save(path, pattern):
    with open(path, 'w') as f:
        s = json.dumps(pattern)
        f.write(s)


t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.tracer(0, 0)


def click(x, y):
    # draw dot
    pos = t.position()
    t.penup()
    t.goto(x, y)
    t.dot()
    t.goto(*pos)
    t.pendown()

    # draw pattern
    pattern.append((x, y))
    if len(pattern) % 4 == 0:
        save(pattern_path, pattern)
        start, end, p1, p2 = pattern[-4:]
        draw_bezier(t, bezier_steps, start, end, p1, p2)
        turtle.update()


# set background image
# img = '/Users/gua/Desktop/heart.gif'
# turtle.bgpic(img)

pattern = load(pattern_path)

draw_pattern(pattern)

# bind mouse click event
turtle.onscreenclick(click)

turtle.update()
turtle.done()
