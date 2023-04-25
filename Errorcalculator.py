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

    def substitute(self, values):
        derivatives_sub = []
        for variable in self.variables:
            # Get the variable name as a string
            variable_name = str(variable)
            # Substitute the values for the variable and error symbol
            derivative_sub = self.derivatives[variable_name].subs(
                {key: sym.UnevaluatedExpr(value) for key, value in values.items()}
            )
            # Format the substituted derivative as a string in LaTeX format
            derivative_latex = sym.latex(derivative_sub)
            derivative_str = f"{values['delta_'+variable_name]} \\cdot {derivative_latex}"
            derivatives_sub.append(derivative_str)
        return " + ".join(derivatives_sub)

    def latex_output(self, values):
        latex_str = "\\begin{align*}\n"
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
        substituted_str = self.substitute(values)
        for value in values.values():
            if value == 0.0:
                continue
            substituted_str = substituted_str.replace(
                f"{value}", "\\SI{" + f"{value}" + "}{}"
            )
        latex_str += f"&= {substituted_str}\\\\\n"
        # Calculate the result using the substituted values
        result = sum(
            [
                values[delta_name]
                * abs(self.derivatives[delta_name.split("_")[1]].subs(values))
                for delta_name in self.error_symbols
            ]
        )
        latex_str += f"&= {result:.6f}\n"
        latex_str += "\\end{align*}\n\n"
        return latex_str

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


a = [38.4]
values2 = {
    "a": 1.2645,
    "b": 60.1,
    "l": 600,
    "delta_a": 0.05,
    "delta_b": 0.06,
    "delta_l": 0.1
}

def my_function1(d, phi): return sym.sin((d+phi)/2)/sym.sin(phi/2)
def avermoegen(a, b, l): return (a*b**2*l)/((l**2-b**2)*sym.sqrt((a*l**2)/(l**2-b)+1))
for x in a:
    values1 = {
        "d": np.radians(x),
        "phi": np.radians(60.1),
        "delta_d": np.radians(0.06),
        "delta_phi": np.radians(0.05),
    }
    derivatives = SymbolicDerivatives(my_function1)
    latex_output = derivatives.latex_output(values1)
    print(latex_output)




