import inspect
import sympy as sym
import numpy as np


class SymbolicDerivatives:
    def __init__(self, func):
        # Get the arguments of the function
        arg_names = inspect.getfullargspec(func).args
        # Define the variables as regular Python variables
        self.variables = [sym.Symbol(name) for name in arg_names]

        # Define the error symbols
        self.error_symbols = ["delta_" + str(variable) for variable in self.variables]

        # Set the function
        self.f = func(*self.variables)

        # Calculate the derivatives and multiply by the errors
        self.derivatives = {}
        for variable in self.variables:
            f_prime = self.f.diff(variable)
            self.derivatives[str(variable)] = f_prime
        print(self.derivatives)

    def substitute(self, values):
        derivatives_sub = []
        for variable in self.variables:
            # Get the variable name as a string
            variable_name = str(variable)
            # Substitute the values for the variable and error symbol
            derivative_sub = self.derivatives[variable_name].subs(
                {key: sym.UnevaluatedExpr(value[0]) for key, value in values.items()}
            )
            # Format the substituted derivative as a string in LaTeX format
            derivative_latex = sym.latex(derivative_sub)
            derivative_str = f"{values['delta_'+variable_name][0]} \\cdot \\left|{derivative_latex} {values['delta_'+variable_name][1]}\\right|"
            derivatives_sub.append(derivative_str)
        return " + ".join(derivatives_sub)

    def latex_output(self, values):
        print('a')
        latex_str = "\\begin{align*}\n"
        print('b')
        latex_str += (
            "&= \\Delta "
            + " + \\Delta ".join(
                [
                    f"{delta_name} \\cdot \\left|{sym.latex(derivative)}\\right|"
                    for delta_name, derivative in self.derivatives.items()
                ]
            )
            + "\\\\\n"
        )
        print('c')
        substituted_str = self.substitute(values)
        print('d')
        for value in values.values():
            if value[0] == 0.0:
                continue
            substituted_str = substituted_str.replace(
                f"{value[0]}", "\\SI{" + f"{value[0]}" + "}{" + f"{value[1]}" + "}"
            )
        latex_str += f"&= {substituted_str}\\\\\n"
        # Calculate the result using the substituted values
        result = sum(
            [
                values[delta_name][0]
                * abs(self.derivatives[delta_name.split("_")[1]].subs({k: v[0] for k, v in values.items()}))
                for delta_name in self.error_symbols
            ]
        )
        latex_str += f"&= \\SI{{{result:.6f}}}{{}}\n"
        latex_str += "\\end{align*}\n\n"
        return latex_str
    def result(self, values):
        result = sum(
            [
                values[delta_name][0]
                * abs(self.derivatives[delta_name.split("_")[1]].subs({k: v[0] for k, v in values.items()}))
                for delta_name in self.error_symbols
            ]
        )
        return result
    def __str__(self):
        derivatives_str = " + ".join(
            [
                f"delta_{variable}*({derivative})"
                for variable, derivative in self.derivatives.items()
            ]
        )
        return derivatives_str

    def __repr__(self):
        return self.__str__()

a = [38.4,38.55,38.6,38.7,38.7,38.85,39.1,39.15,39.5,39.75,39.85]
b = [47.6,48.0,48.1,48.35,48.35,48.65,49.3,49.45,50.45,51.25,51.54]
values2 = {
    "a": (1.2645,''),
    "b": (60.1,''),
    "c": (0.03,''),
    "l": (600,''),
    "delta_a": (0.05,''),
    "delta_b": (0.06,''),
    "delta_l": (0.1,''),
    "delta_c": (0.0005,'')
}

def my_function1(d, phi): return sym.sin((d+phi)/2)/sym.sin(phi/2)

def avermoegen(a, b, c, l): return (c*a*b*l)/((l**2-b**2)*sym.sqrt((a*l**2)/(l**2-b)+1))



for x in b:
    values1 = {
        "d": (np.radians(x), '\\degree'),
        "phi": (np.radians(60.05), '\\degree'),
        "delta_d": (np.radians(0.05), '\\degree'),
        "delta_phi": (np.radians(0.05), '\\degree'),
    }

    derivatives = SymbolicDerivatives(my_function1)
    result = derivatives.result(values1)
    print(result)
    latex_output = derivatives.latex_output(values1)
    print(latex_output)