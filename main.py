"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-04-13
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main func for GLFW OpenGL rendering.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-13 ------------------------
# Requirements and constants
import glfw
import time
import numpy as np

from threading import Thread

from OpenGL.GL import *

from util.glfw_opengl import GLFWWindow, TextAnchor
from ssvep_design import SSVEPLayout


# %% ---- 2025-04-13 ------------------------
# Function and class

def performance_ruler():
    while True:
        time.sleep(10)
        print(f"FPS: {wnd.fps.get_fps()}")
    return


def key_callback(window, key, scancode, action, mods):
    '''Keyboard event callback'''
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        print("ESC is pressed, bye bye.")
        glfw.set_window_should_close(window, True)
    elif action == glfw.PRESS:
        print(f"Key pressed {key}")
    elif action == glfw.RELEASE:
        print(f"Key released {key}")
    elif action == glfw.REPEAT:
        print(f"Key repeated {key}")
    return


def sin(t):
    return np.sin(t*2*np.pi)


def cos(t):
    return np.cos(t*2*np.pi)


def main_render(t: float):
    total = SSVEPLayout.cue_length + SSVEPLayout.blink_length
    n = len(SSVEPLayout.cues)
    this_i = int(t / total) % n + 1

    t %= total

    for i, cue in SSVEPLayout.cues.items():
        s, x, y, w, h = cue
        x += 0.05
        y += 0.05

        if i == this_i and t < SSVEPLayout.cue_length:
            wnd.draw_rect(x-w*0.1, y-h*0.1, w *
                          1.2, h*1.2, (1.0, 0, 0, 1.0))

        c = 0.0
        wnd.draw_rect(x, y, w, h, (c, c, c, 1.0))

        wnd.draw_text(s, x, y, SSVEPLayout.cue_font_scale, TextAnchor.SW, 1.0)

    for i, patch in SSVEPLayout.blinks.items():
        freq, x, y, w, h = patch
        x += 0.05
        y += 0.05

        if t > SSVEPLayout.cue_length:
            c = cos(t*freq) * 0.5 + 0.5
            wnd.draw_rect(x, y, w, h, (c, c, c, 1.0))
        else:
            wnd.draw_rect(x, y, w, h, (1.0, 1.0, 0, 1.0))

    return


# %% ---- 2025-04-13 ------------------------
# Play ground
wnd = GLFWWindow()
wnd.load_font('./font/msyh.ttc')

Thread(target=performance_ruler, daemon=True).start()

wnd.render_loop(key_callback, main_render)

# %% ---- 2025-04-13 ------------------------
# Pending


# %% ---- 2025-04-13 ------------------------
# Pending
