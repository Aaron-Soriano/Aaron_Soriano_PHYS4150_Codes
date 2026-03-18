#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import scipy.constants as c
import seaborn as sns

def bisection(f, guess_neg, guess_pos, error = 1e-15):
    #f: funtion to find the root of
    #guess_pos: float, the negative side of the guessed interval (left side)
    #guess_pos: float, the positve side of the guessed interval (right side)
    #error: float, width of the final interval

    interval = abs(guess_pos - guess_neg)

    iterations = 0 
    while (interval >= error) and (iterations <= 100):
        
        interval = abs(guess_pos - guess_neg)
        guess_mid = guess_neg + interval/2 

        if f(guess_mid) > 0:
            guess_pos = guess_mid
        else:
            guess_neg = guess_mid 

        iterations += 1

    #Best guess for the root is at the middle of the current interval    
    return  guess_neg + interval/2 

def plot_energy_levels():
    
    w = 1e-9 #meters, width of potential well
    V = 20   #eV, depth of potential well 

    lhs = lambda E: np.tan(np.sqrt((w**2 * c.m_e * E * c.e) / (2 * c.hbar**2))) / c.e
    rhs_even = lambda E: np.sqrt((V - E) / E)
    rhs_odd = lambda E: -np.sqrt(E / (V - E))
    
    energy_df = pd.DataFrame({
        "energy" : np.arange(0, 20, 1)
        })
    
    energy_df["lhs"] = lhs(energy_df["energy"])
    energy_df["rhs_odd"] = rhs_even(energy_df["energy"])
    energy_df["rhs_even"] = rhs_odd(energy_df["energy"])
    
    energy_df["left_and_odd"] = energy_df["lhs"] - energy_df["rhs_odd"]
    energy_df["left_and_even"] = energy_df["lhs"] - energy_df["rhs_even"]
    
    fig, ax = plt.subplot_mosaic([
        ["left_and_even_plot", "left_and_odd_plot"],
        ["left_and_both_plot", "left_and_both_plot"]
        ])
    
    sns.lineplot(data = energy_df,
                x = "energy", y = "left_and_odd",
                ax = ax["left_and_odd_plot"])
    ax["left_and_odd_plot"].set_title("Energy for Odd Levels")
    ax["left_and_odd_plot"].set_xlabel("")
    ax["left_and_odd_plot"].set_ylabel("")
    ax["left_and_odd_plot"].grid()

    sns.lineplot(data = energy_df,
                x = "energy", y = "left_and_even",
                ax = ax["left_and_even_plot"]
                )
    ax["left_and_even_plot"].set_title("Energy for Even Levels")
    ax["left_and_even_plot"].set_xlabel("")
    ax["left_and_even_plot"].set_ylabel("")
    ax["left_and_even_plot"].grid()

    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["rhs_odd"],
                            label = "Odd Levels")
    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["rhs_even"],
                            label = "Even Levels")
    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["lhs"],
                            label = "Even Levels")
    ax["left_and_both_plot"].grid()
    ax["left_and_both_plot"].legend()


    #plt.legend()
    plt.xlim((0, 21))
    plt.show()
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("show_points",
                        type = bool,
                        help = "Should the energy levels be shown on the graph",
                        nargs = "?",
                        default = True)   
    args = parser.parse_args()

    plot_energy_levels()
    
    