#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt       

def derivative(f, x, delta_x):

    return (f(x + delta_x) - f(x)) / delta_x

def derivative_and_errors(f_type, f):
    #Plot the derivative
    fig, axis = plt.subplots(1,2)
    derivative_plot, error_plot = axis
    fig.subplots_adjust(wspace = 0.5)

    delta_x = 1e-2

    if f_type == "polynomial":

        f = lambda x: x * (x-1)**2
        f_prime_exact = lambda x: (x-1)**2 + 2*(x-1)*x

    elif f_type == "exponental":
        f = lambda x: np.exp(-x)
        f_prime_exact = lambda x: -np.exp(-x)

    x_coords = np.arange(0,2, delta_x)
    f_prime_coords = derivative(f, x_coords, delta_x)

    derivative_plot.plot(x_coords, f_prime_coords)
    derivative_plot.set_xlabel("X")
    derivative_plot.set_ylabel("f\'(x)")
    derivative_plot.set_title("Derivative of f")

    #Log-Log plot of the errors
    if f_type in ["polynomial", "exponental"]: 
        x = 1
        dx_coords = np.array([1e-2 ** i for i in range(1, 8)])
        e_coords = derivative(f, x, dx_coords) - f_prime_exact(x)

        error_plot.loglog(dx_coords, e_coords)
        error_plot.set_title("Size of Error vs Size of Delta\n(around x=1)")
        error_plot.set_xlabel("Delta")
        error_plot.set_ylabel("Error")
        
    if f_type == "custom":
        error_plot.remove()
    #Final Plot
    plt.show()    

if __name__ == "__main__":    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("funt_kind",
                        type = str,
                        help = """Function to analyse the derivative of:
                        'polynomial': f(x) = x(x-1)^2
                        'exponential': f(x) = e^(-x)
                        'custom': Defined by user in f""",
                        choices = ['polynomial', 'exponential', 'custom'])  
    parser.add_argument("f",
                        type = str,
                        help = "function to analyse the derivative of ",
                        nargs = "?",
                        default = None)   
    args = parser.parse_args()

    exec(f"""def f(x):            #Defining the function
             return {args.f}""")
    derivative_and_errors(args.funt_kind, f)