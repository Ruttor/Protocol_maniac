import inspect
import sympy as sym


class Error:
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
                {key: sym.UnevaluatedExpr(value[0]) for key, value in values.items()}
            )
            # Format the substituted derivative as a string in LaTeX format
            derivative_latex = sym.latex(derivative_sub)
            derivative_str = f"{values['delta_'+variable_name][0]} \\cdot \\left|{derivative_latex}\\right|"
            derivatives_sub.append(derivative_str)
        return " + ".join(derivatives_sub)

    def latex_out(self, values):
        latex_str = "\\begin{align*}\n"
        latex_str += (
            "    &= \\Delta "
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
            if value[0] == 0.0:
                continue
            if int(value[0]) == float(value[0]):
                substituted_str = substituted_str.replace(
                    f"{value[0]}", "\\SI{" + f"{int(value[0])}" + "}{" + f"{value[1]}" + "}"
                )
            else:
                substituted_str = substituted_str.replace(
                    f"{value[0]}", "\\SI{" + f"{float(value[0])}" + "}{" + f"{value[1]}" + "}"
                )
        latex_str += f"    &= {substituted_str}\\\\\n"
        # Calculate the result using the substituted values
        result = sum(
            [
                values[delta_name][0]
                * abs(self.derivatives[delta_name.split("_")[1]].subs({k: v[0] for k, v in values.items()}))
                for delta_name in self.error_symbols
            ]
        )
        latex_str += f"    &= \\SI{{{float(result)}}}{{}}\n"
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
