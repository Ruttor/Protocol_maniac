import errorcalc

def my_function1(a, b):
    return a + a * b ** 3

values1 = {
    "a": (1, '\\volt'),
    "b": (2, ''),
    "delta_a": (0.4, '\\volt'),
    "delta_b": (0.5, ''),
}

derivatives = errorcalc.Error(my_function1)
error = derivatives.result(values1)
latex_out = derivatives.latex_out(values1)
assert error == 9.6
