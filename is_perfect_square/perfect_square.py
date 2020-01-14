from cmath import sqrt
from decimal import localcontext, Decimal


def is_perfect_square(num, *, complex=False):
    if complex:
        res = sqrt(num)
        return int(res.real) == res.real and int(res.imag) == res.imag

    if num < 0:
        return False

    with localcontext() as ctx:
        ctx.prec = 300
        res = Decimal(num).sqrt()

    return int(res) == res
