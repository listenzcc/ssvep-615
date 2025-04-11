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
        1: ('cue1', 0.0, 0.1, 0.25, 0.2),
        2: ('cue2', 0.25, 0.1, 0.25, 0.2),
        3: ('cue3', 0.5, 0.1, 0.25, 0.2),
        4: ('cue4', 0.75, 0.1, 0.25, 0.2),
        5: ('cue5', 0.0, 0.35, 0.25, 0.2),
        6: ('cue6', 0.25, 0.35, 0.25, 0.2),
        7: ('cue7', 0.5, 0.35, 0.25, 0.2),
        8: ('cue8', 0.75, 0.35, 0.25, 0.2),
        9: ('cue9', 0.0, 0.6, 0.25, 0.2),
        10: ('cue10', 0.25, 0.6, 0.25, 0.2),
        11: ('cue11', 0.5, 0.6, 0.25, 0.2),
        12: ('cue12', 0.75, 0.6, 0.25, 0.2),
    }

    # (freq, x, y, w, h)
    blinks = {
        1: (33, 0.0, 0.3, 0.25, 0.05),
        2: (12, 0.25, 0.3, 0.25, 0.05),
        3: (4, 0.5, 0.3, 0.25, 0.05),
        4: (2, 0.75, 0.3, 0.25, 0.05),
        5: (1, 0.0, 0.55, 0.25, 0.05),
        6: (40, 0.25, 0.55, 0.25, 0.05),
        7: (20, 0.5, 0.55, 0.25, 0.05),
        8: (33.7, 0.75, 0.55, 0.25, 0.05),
        9: (15, 0.0, 0.8, 0.25, 0.05),
        10: (25, 0.25, 0.8, 0.25, 0.05),
        11: (10, 0.5, 0.8, 0.25, 0.05),
        12: (5, 0.75, 0.8, 0.25, 0.05),
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
                                  (x + w, y + h), (0, 0, 0, 255), -1)

                cv2.putText(self.image, text, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255, 255), 1, cv2.LINE_AA)
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
