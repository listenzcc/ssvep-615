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
import pandas as pd

from threading import Thread

from OpenGL.GL import *

from util.glfw_opengl import GLFWWindow, TextAnchor
from util.logging import logger
from ssvep_design import SSVEPLayout


# %% ---- 2025-04-13 ------------------------
# Function and class
class DataBuffer:
    data = []

    def collect(self, i, t, c):
        self.data.append((i, t, c))

    def save(self):
        df = pd.DataFrame(self.data, columns=['i', 't', 'c'])
        df.to_excel('a.xlsx')


db = DataBuffer()


class StopWatch:
    running: bool = False
    tic: float = time.time()

    def start(self):
        self.tic = time.time()
        self.running = True
        logger.info('Start running.')

    def stop(self):
        self.running = False
        logger.info('Stop running.')

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def peek(self):
        return time.time() - self.tic


sw = StopWatch()


def performance_ruler():
    while True:
        time.sleep(10)
        print(f"FPS: {wnd.fps.get_fps()}")
    return


def key_callback(window, key, scancode, action, mods):
    '''Keyboard event callback'''
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        print("ESC is pressed, bye bye.")
        # db.save()
        glfw.set_window_should_close(window, True)
        return
    elif action == glfw.PRESS:
        print(f"Key pressed {key}")
    elif action == glfw.RELEASE:
        # print(f"Key released {key}")
        return
    elif action == glfw.REPEAT:
        # print(f"Key repeated {key}")
        return

    try:
        c = chr(key)
        if c == 'S':
            sw.toggle()
    except Exception as e:
        pass

    return


def sin(t):
    return np.sin(t*2*np.pi)


def cos(t):
    return np.cos(t*2*np.pi)


def main_render():
    t = sw.peek()

    total = SSVEPLayout.cue_length + SSVEPLayout.blink_length
    n = len(SSVEPLayout.cues)
    this_i = int(t / total) % n + 1

    t_in_trial = t % total

    for i, patch in SSVEPLayout.blinks.items():
        freq, x, y, w, h = patch
        x += 0.05
        y += 0.05

        if sw.running:
            if t_in_trial > SSVEPLayout.cue_length:
                # Draw blink
                c = cos(t*freq) * 0.5 + 0.5
                wnd.draw_rect(x, y, w, h, (c, c, c, 1.0))
                # if i == 1:
                #     db.collect(this_i, t, c)
                #     print(this_i, t, c)
            else:
                # Draw green
                wnd.draw_rect(x, y, w, h, (0.0, 1.0, 0, 1.0))
        else:
            # Draw yellow
            wnd.draw_rect(x, y, w, h, (1.0, 1.0, 0.0, 1.0))
            c = cos(t+x+y) * 0.5 + 0.5
            wnd.draw_rect(x, y, w, h, (c, c, c, 1.0))

        wnd.draw_text(f'{freq}', x, y,
                      SSVEPLayout.blink_font_scale, TextAnchor.SW, 1.0)

    for i, cue in SSVEPLayout.cues.items():
        s, x, y, w, h = cue
        x += 0.05
        y += 0.05

        if i == this_i and t_in_trial < SSVEPLayout.cue_length:
            wnd.draw_rect(x-w*0.1, y-h*0.1, w *
                          1.2, h*1.2, (1.0, 0, 0, 1.0))

        c = 0.0
        wnd.draw_rect(x, y, w, h, (c, c, c, 1.0))

        wnd.draw_text(s, x, y, SSVEPLayout.cue_font_scale, TextAnchor.SW, 1.0)

    if not sw.running:
        wnd.draw_text('Press s to start.', (t/10) % 1, 0.5,
                      1, TextAnchor.CENTER, color=1.0)

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
