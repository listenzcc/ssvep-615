"""
File: analysis-high.py
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
import cv2
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

VIDEO_PATH = "high-speed-2.mp4"
FPS = 120


# %% ---- 2025-04-14 ------------------------
# Function and class

def compute_pixel_timeseries(video_path):
    """
    Reads a video file and computes the timeseries of a specific pixel's value.

    Args:
        video_path (str): Path to the video file.

    Returns:
        list: Timeseries of the pixel's intensity values.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {video_path}")

    timeseries = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Assuming the video is in color (BGR), convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 38
        pixel_value = np.mean(gray_frame[450:470, 400-20:400+20])

        # 33.2
        pixel_value = np.mean(gray_frame[1200:1250, 400-20:400+20])

        timeseries.append(pixel_value)

    cap.release()
    return timeseries, gray_frame


def get_video_fps(video_path):
    """
    Retrieves the frames per second (FPS) of a video.

    Args:
        video_path (str): Path to the video file.

    Returns:
        float: Frames per second (FPS) of the video.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    if fps == 0:
        raise ValueError("FPS value is zero, cannot retrieve FPS.")

    return fps


# %% ---- 2025-04-14 ------------------------
# Play ground

if __name__ == "__main__":
    # Compute the timeseries for the specified pixel
    pixel_timeseries, gray_frame = compute_pixel_timeseries(
        VIDEO_PATH)

    # Retrieve and display the FPS of the video
    fps = get_video_fps(VIDEO_PATH)
    print(f"Frames per second (FPS): {fps:.2f}")

    times = np.linspace(0, len(pixel_timeseries) /
                        FPS, len(pixel_timeseries))

    # Calculate the real time interval between frames
    frame_time_interval = 1.0 / fps
    print(f"Time interval between frames: {frame_time_interval:.6f} seconds")

    # Plot the timeseries
    # plt.plot(np.arange(len(pixel_timeseries)) *
    #          frame_time_interval, pixel_timeseries)
    plt.plot(times, pixel_timeseries)
    plt.title(f"Pixel Intensity Timeseries")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Intensity")
    plt.show()

    plt.imshow(gray_frame)
    plt.show()

    fig = px.line(
        # x=np.arange(len(pixel_timeseries)) * frame_time_interval,
        x=times,
        y=pixel_timeseries, labels={'x': 'Time (seconds)', 'y': 'Intensity'})
    fig.show()

    # Compute spectrum power
    m = (times > 2) * (times < 3)
    ts_high = np.array(pixel_timeseries)[m]
    ts_high -= np.mean(ts_high)
    plt.plot(ts_high)
    plt.show()
    freqs_high = np.fft.rfftfreq(len(ts_high), d=1/FPS)
    spectrum_power_high = np.abs(np.fft.rfft(ts_high))**2
    fig = px.line(x=freqs_high, y=spectrum_power_high,
                  title='Spectrum Power of 33.2 Hz.')
    fig.show()

# %% ---- 2025-04-14 ------------------------
# Pending


# %% ---- 2025-04-14 ------------------------
# Pending
