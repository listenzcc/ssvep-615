"""
File: ssvep_design.py
Author: Chuncheng Zhang
Date: 2025-04-11
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    SSVEP design.

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
import math
import cv2
import numpy as np
from util.logging import logger
from util.window import ImageScreen


# %% ---- 2025-04-11 ------------------------
# Function and class
class SSVEPLayout:
    # (text, x, y, w, h)
    cues = {
        1: ('cue1', 0.0, 0.0, 0.15, 0.15),
        2: ('cue2', 0.2, 0.0, 0.15, 0.15),
        3: ('cue3', 0.4, 0.0, 0.15, 0.15),
        4: ('cue4', 0.6, 0.0, 0.15, 0.15),
        5: ('cue5', 0.8, 0.0, 0.15, 0.15),
        6: ('cue6', 0.0, 0.2, 0.15, 0.15),
        7: ('cue7', 0.2, 0.2, 0.15, 0.15),
        8: ('cue8', 0.4, 0.2, 0.15, 0.15),
        9: ('cue9', 0.6, 0.2, 0.15, 0.15),
        10: ('cue10', 0.8, 0.2, 0.15, 0.15),
        11: ('cue11', 0.0, 0.4, 0.15, 0.15),
        12: ('cue12', 0.2, 0.4, 0.15, 0.15),
        13: ('cue13', 0.4, 0.4, 0.15, 0.15),
        14: ('cue14', 0.6, 0.4, 0.15, 0.15),
        15: ('cue15', 0.8, 0.4, 0.15, 0.15),
        16: ('cue16', 0.0, 0.6, 0.15, 0.15),
        17: ('cue17', 0.2, 0.6, 0.15, 0.15),
        18: ('cue18', 0.4, 0.6, 0.15, 0.15),
        19: ('cue19', 0.6, 0.6, 0.15, 0.15),
        20: ('cue20', 0.8, 0.6, 0.15, 0.15),
        21: ('cue21', 0.0, 0.8, 0.15, 0.15),
        22: ('cue22', 0.2, 0.8, 0.15, 0.15),
        23: ('cue23', 0.4, 0.8, 0.15, 0.15),
        24: ('cue24', 0.6, 0.8, 0.15, 0.15),
        25: ('cue25', 0.8, 0.8, 0.15, 0.15),
    }

    # (freq, x, y, w, h)
    blinks = {
        1: (10, 0.0, 0.15, 0.15, 0.05),
        2: (12, 0.2, 0.15, 0.15, 0.05),
        3: (15, 0.4, 0.15, 0.15, 0.05),
        4: (20, 0.6, 0.15, 0.15, 0.05),
        5: (25, 0.8, 0.15, 0.15, 0.05),
        6: (30, 0.0, 0.35, 0.15, 0.05),
        7: (33, 0.2, 0.35, 0.15, 0.05),
        8: (40, 0.4, 0.35, 0.15, 0.05),
        9: (50, 0.6, 0.35, 0.15, 0.05),
        10: (60, 0.8, 0.35, 0.15, 0.05),
        11: (70, 0.0, 0.55, 0.15, 0.05),
        12: (80, 0.2, 0.55, 0.15, 0.05),
        13: (90, 0.4, 0.55, 0.15, 0.05),
        14: (100, 0.6, 0.55, 0.15, 0.05),
        15: (110, 0.8, 0.55, 0.15, 0.05),
        16: (120, 0.0, 0.75, 0.15, 0.05),
        17: (130, 0.2, 0.75, 0.15, 0.05),
        18: (140, 0.4, 0.75, 0.15, 0.05),
        19: (150, 0.6, 0.75, 0.15, 0.05),
        20: (160, 0.8, 0.75, 0.15, 0.05),
        21: (170, 0.0, 0.95, 0.15, 0.05),
        22: (180, 0.2, 0.95, 0.15, 0.05),
        23: (190, 0.4, 0.95, 0.15, 0.05),
        24: (200, 0.6, 0.95, 0.15, 0.05),
        25: (210, 0.8, 0.95, 0.15, 0.05),
    }


class SSVEPImageScreen(ImageScreen):
    def __init__(self):
        super().__init__()
        logger.info('SSVEPImageScreen initialized.')

    def draw_cues(self, highlight=None):
        for k, cue in SSVEPLayout.cues.items():
            text, x, y, w, h = cue
            x = int(x * self.image.shape[1])
            y = int(y * self.image.shape[0])
            w = int(w * self.image.shape[1])
            h = int(h * self.image.shape[0])

            with self.lock:
                if highlight == k:
                    cv2.rectangle(self.image, (x, y),
                                  (x + w, y + h), (0, 0, 255, 255), -1)
                else:
                    cv2.rectangle(self.image, (x, y),
                                  (x + w, y + h), (0, 0, 0, 200), -1)

                cv2.putText(self.image, text, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 255, 255, 255), 1, cv2.LINE_AA)
        pass

    def draw_blinks(self):
        t = time.time()
        for k, blink in SSVEPLayout.blinks.items():
            freq, x, y, w, h = blink
            x = int(x * self.image.shape[1])
            y = int(y * self.image.shape[0])
            w = int(w * self.image.shape[1])
            h = int(h * self.image.shape[0])

            c = int(255 * (math.sin(freq * t * 2 * math.pi) * 0.5 + 0.5))

            with self.lock:
                cv2.rectangle(self.image, (x, y),
                              (x + w, y + h), (c, c, c, 255), -1)
                cv2.putText(self.image, str(freq), (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255, 255), 1, cv2.LINE_AA)
        pass


# %% ---- 2025-04-11 ------------------------
# Play ground


# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
