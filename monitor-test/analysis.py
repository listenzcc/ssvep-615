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
import mne
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from pathlib import Path
from scipy import signal


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
input_1Hz = np.sin(2*np.pi*1*r1.times)
output_1Hz = d1[-2]
output_unknown = d2[-2]
fs = 1000

# ================= 核心算法 =================


def estimate_transfer_function(u, y, fs):
    """从输入u和输出y估计频率响应函数"""
    # 使用Welch方法估计频响(抗噪声能力强)
    f, H = signal.csd(y, u, fs=fs, nperseg=1024)  # 交叉功率谱密度
    _, Pxx = signal.welch(u, fs=fs, nperseg=1024)  # 输入功率谱
    H = H / Pxx  # 频响函数估计
    return f, H


def restore_input(y, f_est, H_est, fs):
    """从输出y还原输入信号"""
    # 计算输出频谱
    y_fft = np.fft.fft(y)
    freqs = np.fft.fftfreq(len(y), 1/fs)

    # 插值得到完整频响
    H_mag = np.interp(np.abs(freqs), f_est, np.abs(H_est), left=0, right=0)
    H_phase = np.interp(np.abs(freqs), f_est, np.unwrap(
        np.angle(H_est)), left=0, right=0)
    H_full = H_mag * np.exp(1j*H_phase)

    # 频域反演 (避免除以零)
    epsilon = 1e-10
    x_fft = y_fft / (H_full + epsilon)
    return np.fft.ifft(x_fft).real


# 步骤1：估计系统频响
f_est, H_est = estimate_transfer_function(input_1Hz, output_1Hz, fs)

# 步骤2：还原未知输入
restored_input = restore_input(output_unknown, f_est, H_est, fs)

# ================= 结果分析 =================
plt.figure(figsize=(12, 8))

# 1. 频响估计结果
plt.subplot(2, 1, 1)
plt.semilogy(f_est, np.abs(H_est))
plt.title('Estimated Frequency Response (from 1Hz excitation)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)

# 2. 还原信号展示（因为没有真实未知输入，只显示还原结果）
plt.subplot(2, 1, 2)
plt.plot(r2.times[:2000], restored_input[:2000])  # 显示前2秒
plt.title('Restored Unknown Input Signal')
plt.xlabel('Time (s)')
plt.grid(True)

plt.tight_layout()
plt.show()
# %%
# %%
# %%
# %%
