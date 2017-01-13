from math import sin, cos

e_t = 10.0

def x_t(t):
    return sin(t) * 100.0 / (1.0 + t)

def y_t(t):
    return cos(t) * 100.0 / (1.0 + t)
