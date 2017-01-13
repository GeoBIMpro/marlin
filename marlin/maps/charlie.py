from math import sin, cos

e_t = 80.0

def x_t(t):
    if t > 63.0:
        return (t - 63.0) + x_t(63.0)
    if t > 60.0:
        return -sin(t - 60.0) * 5.0 + x_t(60.0)

    if t > 32:
        return -(t - 32) + x_t(32)
    if t > 30.0:
        return sin(t - 30.0) * 5.0 + x_t(30.0)
    return t

def y_t(t):
    if t > 63.0:
        return 0.0 + y_t(63.0)
    if t > 60.0:
        return cos(t - 60.0) * 5.0 - 5.0 + y_t(60.0)

    if t > 32:
        return -(t - 32) + y_t(32)
    if t > 30.0:
        return cos(t - 30.0) * 5.0 - 5.0 + y_t(30.0)
    return 0
