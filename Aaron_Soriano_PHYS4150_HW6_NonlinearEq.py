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

def estimate_energy_levels(energy_min, energy_max):
    #energy_min, energy_max: eV, range to find energy levels

    w = 1e-9 #meters, width of potential well
    V = 20   #eV, depth of potential well 

    lhs = lambda E: np.tan(np.sqrt((w**2 * c.m_e * E * c.e) / (2 * c.hbar**2))) / c.e
    rhs_even = lambda E: np.sqrt((V - E) / E)
    rhs_odd = lambda E: -np.sqrt(E / (V - E))
    
    energy_df = pd.DataFrame({
        "energy" : np.linspace(energy_min, energy_max, 100)
        })
    
    energy_df["lhs"] = lhs(energy_df["energy"])
    energy_df["rhs_odd"] = rhs_even(energy_df["energy"])
    energy_df["rhs_even"] = rhs_odd(energy_df["energy"])
    
    energy_df["left_and_odd"] = energy_df["lhs"] - energy_df["rhs_odd"]   
    energy_df["left_and_even"] = energy_df["lhs"] - energy_df["rhs_even"]


    level_boundaries = []
    for i in range(len(energy_df["left_and_odd"]) - 1):
        
        #find sign changes in left_and_odd
        point_i = energy_df.at[i, "left_and_odd"]
        point_i1 = energy_df.at[i + 1, "left_and_odd"]
  
        if np.sign(point_i) != np.sign(point_i1):
            point_i = energy_df.at[i, "energy"]
            point_i1 = energy_df.at[i + 1, "energy"]
            level_boundaries.append((point_i, point_i1, "odd")) 
        
        #find sign changes in left_and_even
        point_i = energy_df.at[i, "left_and_even"]
        point_i1 = energy_df.at[i + 1, "left_and_even"]
  
        if np.sign(point_i) != np.sign(point_i1):
            point_i = energy_df.at[i, "energy"]
            point_i1 = energy_df.at[i + 1, "energy"]
            level_boundaries.append((point_i, point_i1, "even"))    
    
    even_roots = []
    odd_roots = []
    for neg_bd, pos_bd, parity in level_boundaries:
        
        if parity == "even":
            f = lambda x: lhs(x) - rhs_even(x)
            root = bisection(f, neg_bd, pos_bd)
            even_roots.append(root)

        else:
            f = lambda x: lhs(x) - rhs_odd(x)   
            root = bisection(f, neg_bd, pos_bd)
            odd_roots.append(root)

    return energy_df, (even_roots, odd_roots)

def plot_energy_levels(energy_df, roots = []):

    
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
                ax = ax["left_and_even_plot"])
    ax["left_and_even_plot"].set_title("Energy for Even Levels")
    ax["left_and_even_plot"].set_xlabel("")
    ax["left_and_even_plot"].set_ylabel("")
    ax["left_and_even_plot"].grid()

    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["rhs_odd"],
                            label = "Odd Levels")
    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["rhs_even"],
                            label = "Even Levels")
    ax["left_and_both_plot"].plot(energy_df["energy"], energy_df["lhs"],
                            label = "")
    ax["left_and_both_plot"].set_xlabel("Energy (eV)")
    ax["left_and_both_plot"].set_ylabel("Potental")
    ax["left_and_both_plot"].grid()
    ax["left_and_both_plot"].legend()

    if roots:

        w = 1e-9 #meters, width of potential well
        V = 20   #eV, depth of potential well 

        lhs = lambda E: np.tan(np.sqrt((w**2 * c.m_e * E * c.e) / (2 * c.hbar**2))) / c.e
        rhs_even = lambda E: np.sqrt((V - E) / E)
        rhs_odd = lambda E: -np.sqrt(E / (V - E))

        even_roots, odd_roots = roots
        
        for root in even_roots:

            ax["left_and_even_plot"].axvline(root)
            ax["left_and_both_plot"].axvline(root, color = "blue")
    

        for root in odd_roots:
            ax["left_and_odd_plot"].axvline(root)  
            ax["left_and_both_plot"].axvline(root, color = "orange")  
    

        #for root in even_roots:
            
        #    ax["left_and_even_plot"].annotate(
        #        f"{root[0]:.3f}",
        #        xy=(root[0], root[1]), xycoords='data',
        #        xytext=(1.5, 1.5), textcoords='offset points')
            
    #plt.legend()
    plt.tight_layout()        
    plt.xlim((0, 21))
    plt.show()
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("show_points",
                        type = bool,
                        help = "Should the energy levels be shown on the graph",
                        nargs = "?",
                        default = True)   
    parser.add_argument("lower_limit",
                        type = float,
                        help = "The lower limit to search for energy levels in eV",
                        nargs = "?",
                        default = 0)   
    parser.add_argument("upper_limit",
                        type = float,
                        help = "The upper limit to search for energy levels in eV",
                        nargs = "?",
                        default = 20) 
    args = parser.parse_args()

    energy_df, roots = estimate_energy_levels(args.lower_limit, args.upper_limit) 
    if args.show_points:
        plot_energy_levels(energy_df, roots = roots)

    else:
        plot_energy_levels(energy_df)
    
    