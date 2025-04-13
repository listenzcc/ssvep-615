"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-04-11
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main entry point of the program.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-11 ------------------------
# Requirements and constants
import sys
from PyQt6.QtCore import Qt, QTimer

from util.logging import logger
from util.window import BasicScreen, ImageScreen
from ssvep_design import SSVEPImageScreen

my_screen = SSVEPImageScreen()

# %% ---- 2025-04-11 ------------------------
# Function and class


def _about_to_quit():
    logger.info('Application is about to quit.')
    return


def _on_key_pressed(event):
    key = event.key()
    qt_key = Qt.Key(key)

    if qt_key == Qt.Key.Key_Escape:
        logger.info('Escape key pressed. Closing the application.')
        my_screen.qapp.quit()
    elif qt_key == Qt.Key.Key_Space:
        logger.info('Space key pressed. Doing nothing.')
    else:
        logger.info(f'Key {key} pressed. Doing nothing.')

    return


draw_cues_only_once = True


def _on_time_tick():
    my_screen.frc.update()
    my_screen.update_clock()

    global draw_cues_only_once
    if draw_cues_only_once:
        my_screen.draw_cues()
        draw_cues_only_once = False

    my_screen.draw_blinks()
    my_screen.put_image()
    return


# %% ---- 2025-04-11 ------------------------
# Play ground
my_screen.qapp.aboutToQuit.connect(_about_to_quit)
my_screen.window.keyReleaseEvent = _on_key_pressed

timer = QTimer()
timer.timeout.connect(_on_time_tick)
timer.start()

my_screen.show_window()
sys.exit(my_screen.qapp.exec())

# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
