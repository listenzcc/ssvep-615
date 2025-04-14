"""
File: experiment.py
Author: Chuncheng Zhang
Date: 2025-04-14
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-14 ------------------------
# Requirements and constants
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


# %% ---- 2025-04-14 ------------------------
# Function and class

def generate_sine_wave(freq=1, repeats=10, sample_rate=100):
    """
    Generate a sine wave signal.

    Args:

        freq (float): Frequency of the sine wave in Hz.
        repeats (int): How many T of the sine wave.
        sample_rate (int): Number of samples per second.

    Returns:
        np.ndarray: Array containing the sine wave signal.
    """
    duration = int(repeats / freq)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t), t


def draw_detail(ts, times):
    plt.plot(times, ts)
    plt.show()

    freqs = np.fft.rfftfreq(len(ts), d=1/100)
    spectrum_power = np.abs(np.fft.rfft(ts))**2
    fig = px.line(x=freqs, y=spectrum_power,
                  title='Spectrum Power.')
    fig.show()
    return


# %% ---- 2025-04-14 ------------------------
# Play ground
# Example usage
ts, times = generate_sine_wave()
print(ts.shape)

draw_detail(ts, times)

d = ts.reshape((10, 100))
print(d.shape)
select1 = list(range(d.shape[1]))
np.random.shuffle(select1)

rnd = list(range(d.shape[1]))
np.random.shuffle(rnd)
np.random.shuffle(d[:, ::3].T)
# d = d[:, rnd]

ts = d.ravel()
draw_detail(ts, times)

# %%

# %% ---- 2025-04-14 ------------------------
# Pending


# %% ---- 2025-04-14 ------------------------
# Pending
