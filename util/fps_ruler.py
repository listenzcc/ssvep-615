"""
File: fps_ruler.py
Author: Chuncheng Zhang
Date: 2025-04-11
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Frame rate counter.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-11 ------------------------
# Requirements and constants

import time
from collections import deque


# %% ---- 2025-04-11 ------------------------
# Function and class

class FPSRuler:
    def __init__(self, max_samples=100):
        """
        Initialize the frame rate counter.

        Args:
            max_samples (int): Maximum number of timestamps to store for calculating frame rate.
        """
        self.timestamps = deque(maxlen=max_samples)

    def update(self):
        """
        Update the frame rate counter with the current timestamp.
        """
        self.timestamps.append(time.time())

    def get_fps(self):
        """
        Calculate and return the current frame rate.

        Returns:
            float: The calculated frame rate, or 0.0 if not enough data is available.
        """
        if len(self.timestamps) < 2:
            return 0.0
        time_deltas = [self.timestamps[i] - self.timestamps[i - 1]
                       for i in range(1, len(self.timestamps))]
        avg_delta = sum(time_deltas) / len(time_deltas)
        rate = 1.0 / avg_delta if avg_delta > 0 else 0.0
        # print(rate)
        return rate


# %% ---- 2025-04-11 ------------------------
# Play ground

if __name__ == "__main__":
    # Example usage of FrameRateCounter
    frc = FPSRuler(max_samples=10)
    for _ in range(20):
        frc.update()
        print(f"Current Frame Rate: {frc.get_fps():.2f} FPS")
        time.sleep(0.1)


# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
