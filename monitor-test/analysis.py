"""
File: analysis.py
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
import mne
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path


# %% ---- 2025-04-14 ------------------------
# Function and class
r1 = mne.io.read_raw_cnt('low.cnt')
r2 = mne.io.read_raw_cnt('high_30.cnt')
print(r1, r2)
print(r1.info)
print(r1.info['ch_names'])


# %% ---- 2025-04-14 ------------------------
# Play ground
# mne.viz.plot_raw(r1)
# mne.viz.plot_raw(r2)


# %% ---- 2025-04-14 ------------------------
# Pending
d1 = r1.get_data()
ts = d1[-2]
fig = px.line(x=r1.times, y=ts, title='low.cnt')
fig.show()

d2 = r2.get_data()
ts = d2[-2]
fig = px.line(x=r2.times, y=ts, title='high_30.cnt')
fig.show()


# %% ---- 2025-04-14 ------------------------
# Pending
# Compute the spectrum power of the ts

# Compute spectrum power for low.cnt
ts = d1[-2]
freqs = np.fft.rfftfreq(len(ts), d=1/r1.info['sfreq'])
spectrum_power = np.abs(np.fft.rfft(ts))**2
fig = px.line(x=freqs, y=spectrum_power, title='Spectrum Power of low.cnt')
fig.show()

# Compute spectrum power for high_30.cnt
ts_high = d2[-2]
freqs_high = np.fft.rfftfreq(len(ts_high), d=1/r2.info['sfreq'])
spectrum_power_high = np.abs(np.fft.rfft(ts_high))**2
fig = px.line(x=freqs_high, y=spectrum_power_high,
              title='Spectrum Power of high_30.cnt')
fig.show()

# %%
files = Path('.').iterdir()
for file in files:
    if not file.name.endswith('.cnt'):
        continue
    print(file)
    raw = mne.io.read_raw_cnt(file)
    times = raw.times
    d = raw.get_data()
    ts = d[-2]
    freqs_high = np.fft.rfftfreq(len(ts), d=1/raw.info['sfreq'])
    spectrum_power_high = np.abs(np.fft.rfft(ts))**2
    fig = px.line(x=freqs_high, y=spectrum_power_high,
                  title=f'Spectrum Power of {file.name}')
    fig.show()


# %%
# %%
# %%
