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
from util.logging import logger
from util.window import ImageScreen, small_font


# %% ---- 2025-04-11 ------------------------
# Function and class
class SSVEPLayout:
    # (text, x, y, w, h)
    cues = {
        1: ('cue1', 0.1, 0.3, 0.1, 0.2),
        2: ('cue2', 0.3, 0.3, 0.1, 0.2),
        3: ('cue3', 0.5, 0.3, 0.1, 0.2),
        4: ('cue4', 0.7, 0.3, 0.1, 0.2),
    }

    # (freq, x, y, w, h)
    blinks = {
        1: (33, 0.1, 0.5, 0.1, 0.2),
        2: (12, 0.3, 0.5, 0.1, 0.2),
        3: (4, 0.5, 0.5, 0.1, 0.2),
        4: (2, 0.7, 0.5, 0.1, 0.2),
    }


class SSVEPImageScreen(ImageScreen):
    def __init__(self):
        super().__init__()
        logger.info('SSVEPImageScreen initialized.')

    def draw_cues(self, highlight=None):
        for k, cue in SSVEPLayout.cues.items():
            text, x, y, w, h = cue
            x = int(x * self.image.width)
            y = int(y * self.image.height)
            w = int(w * self.image.width)
            h = int(h * self.image.height)

            with self.lock:
                if highlight == k:
                    self.image_draw.rectangle(
                        [x, y, x + w, y + h], fill=(255, 0, 0))
                else:
                    self.image_draw.rectangle(
                        [x, y, x + w, y + h], fill=(0, 0, 0))

                self.image_draw.text((x + 5, y + 5), text,
                                     font=small_font, fill=(255, 255, 255))
        pass

    def draw_blinks(self):
        t = time.time()
        for k, blink in SSVEPLayout.blinks.items():
            freq, x, y, w, h = blink
            x = int(x * self.image.width)
            y = int(y * self.image.height)
            w = int(w * self.image.width)
            h = int(h * self.image.height)

            c = int(255*(math.sin(freq * t * 2 * math.pi) * 0.5 + 0.5))

            with self.lock:
                self.image_draw.rectangle([x, y, x + w, y + h], fill=(c, c, c))
                self.image_draw.text((x + 5, y + 5), str(freq),
                                     font=small_font, fill=(255, 255, 255))
        pass


# %% ---- 2025-04-11 ------------------------
# Play ground


# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
