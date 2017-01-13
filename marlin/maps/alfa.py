e_t = 100.0

def x_t(t):
    return t

def y_t(t):
    if t > 75:
        return - (t - 75.0) / 4.0 + y_t(75.0)
    if t > 50.0:
        return 0.0 + y_t(50.0)
    if t > 25.0:
        return (t - 25.0) / 4.0 + y_t(25.0)
    return 0
