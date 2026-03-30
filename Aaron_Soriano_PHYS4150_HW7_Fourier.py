#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy.fft import rfft
import numpy as np
import argparse
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns      

def square_wave(x):
    #Inputs: x: an array of the points to sample from
    #Returns the coordsinates of a single cycle of a square wave, sampled over the points in `x`
    
    N = len(x)
    wave = np.zeros(N)
    wave[ : N//2] = 1    #Positive half of the wave 
    wave[N//2 : ] = -1   #Begative half of the wave 
    
    return wave

def sawtooth_wave(x):
    #Inputs: x: an array of the points to sample from
    #Returns the coordsinates of a single cycle of a sawtooth wave, sampled over the points in `x`
    
    return x

def modulated_sine(x):
    #Inputs: x: an array of the points to sample from
    #Returns the coordsinates of sin(pi*x/N) * sin(20pi*x/N), sampled over the points in `x`
    
    N = len(x)
    f = lambda n: np.sin(np.pi * n / N) * np.sin(20*np.pi * n / N)
    
    return f(x)

def plot_functs_and_freqs(plot_type, N = 1000):
    #Inputs: `plot_type`: str, which of the three functions to plot
    #        `N` : int, number of evenly spaced points to sample the functions 
    #Displays a plot of the function in `plot_type` and a plot of its Fourier transform 
    
    waves = {
        "square" : square_wave,
        "saw"    : sawtooth_wave,
        "mod_sin": modulated_sine
    }
    
    #Setting up dataframes
    samples_df = pd.DataFrame({
        "x" : np.linspace(-1, 1, N)
    })
    samples_df[plot_type] = waves[plot_type](samples_df["x"])

    intensity = rfft(samples_df[plot_type] - np.mean(samples_df[plot_type]))
    frequency = np.arange(0, len(intensity))

    freq_df = pd.DataFrame({
        "freq": frequency / N,
        "intensity": intensity / np.absolute(intensity)
    })

    #Ploting

    plain_names = {
        "square" : "Square Wave",
        "saw"    : "Sawtooth Wave",
        "mod_sin": "Modulated Sine Wave"
    }
    
    fig, ax = plt.subplot_mosaic([
        ["amp_plot"],
        ["freq_plot"]
        ])
    plt.suptitle(f"Plot of {plain_names[plot_type]} and Frequency Spectrum")

    sns.lineplot(data = samples_df,
                x = "x", y = plot_type,
                ax = ax["amp_plot"])
    ax["amp_plot"].set_title(f"Amplitude Plot of {plain_names[plot_type]}")
    ax["amp_plot"].set_xlabel("Time")
    ax["amp_plot"].set_ylabel("Amplitude")

    sns.lineplot(data = freq_df,
                x = "freq", y = "intensity",
                ax = ax["freq_plot"])
    ax["freq_plot"].set_title(f"Frequency Spectrum of {plain_names[plot_type]}")
    ax["freq_plot"].set_xlabel("Frequency")
    ax["freq_plot"].set_ylabel("Intensity")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("plot_type",
                        type = str,
                        help = """Which of the three functions to plot:
                        'square'  : One cycle of a square wave
                        'saw'     : One cycle of a sawtooth wave
                        'mod_sin' : A modulated sine wave y_n = sin( n *pi / N)sin(n * 20*pi / N)""",
                        choices = ["square", "saw", "mod_sin"])
    parser.add_argument("points",
                        type = int,
                        help = """Number of sampling points in the wave""",
                        nargs = "?",
                        default = 1000)
    args = parser.parse_args()

    plot_functs_and_freqs(args.plot_type, args.points)