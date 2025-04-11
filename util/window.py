"""
File: window.py
Author: Chuncheng Zhang
Date: 2025-04-11
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Qt window.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-11 ------------------------
# Requirements and constants
from PIL import Image
from PIL.ImageQt import ImageQt
import time
from datetime import datetime
from threading import Thread, RLock
import sys
import cv2
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QImage
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from .logging import logger
from .frame_rate_counter import FrameRateCounter

# Initialize the QApplication in the first place.
qapp = QApplication(sys.argv)

# %% ---- 2025-04-11 ------------------------
# Function and class


class BasicScreen:
    qapp = qapp
    window = QMainWindow()
    pixmap_label = QLabel(window)
    width = 800
    height = 600

    def __init__(self) -> None:
        self.prepare_window()
        pass

    def show_window(self):
        self.window.show()
        logger.info(f'Window shown with size: {self.width}x{self.height}')
        return

    def prepare_window(self):
        '''
        Prepare the window,
        - Set its size, position and transparency.
        - Set the self.pixmap_container geometry accordingly.
        '''
        # Translucent image by its RGBA A channel
        self.window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Disable frame and keep the window on the top layer
        # It is necessary to set the FramelessWindowHint for the WA_TranslucentBackground works
        self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                                   Qt.WindowType.WindowStaysOnTopHint)

        # Set overall opacity.
        overall_opacity = 1.0
        self.window.setWindowOpacity(overall_opacity)

        # Fetch the screen size and set the size for the window
        screen = self.qapp.primaryScreen()
        screen_width = screen.size().width()
        screen_height = screen.size().height()

        # Make it full-screen
        self.width = screen.size().width()
        self.height = screen.size().height()

        # Set the window size
        self.window.resize(self.width, self.height)

        # Put the window to the right
        self.window.move(screen_width-self.width, 0)

        # Set the pixmap_label accordingly,
        # and it is within the window bounds
        self.pixmap_label.setGeometry(0, 0, self.width, self.height)
        # self.pixmap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.pixmap_label.setScaledContents(True)

        logger.debug(
            f'Reset window size to {self.width}, {self.height}, and reset other stuff')
        return


class ImageScreen(BasicScreen):
    background_color = (0, 0, 0, 100)  # RGBA

    def __init__(self, image: np.ndarray = None) -> None:
        super().__init__()
        self.lock = RLock()
        self.frc = FrameRateCounter(max_samples=100)
        self.mk_image(image)
        self.put_image()
        logger.info('ImageQtWindow initialized.')
        pass

    def put_image(self, image: np.ndarray = None):
        '''
        Put the image to the pixmap_label.
        '''
        if image is not None:
            self.image = image
        with self.lock:
            # Convert BGRA to RGBA
            image_rgba = cv2.cvtColor(self.image, cv2.COLOR_BGRA2RGBA)
            height, width, channel = image_rgba.shape
            bytes_per_line = channel * width

            # Create QImage with correct format
            q_image = QPixmap.fromImage(
                QImage(image_rgba.data, width, height,
                       bytes_per_line, QImage.Format.Format_RGBA8888)
            )

        self.pixmap_label.setPixmap(q_image)
        return

    def get_image(self) -> np.ndarray:
        '''
        Get the image from the pixmap_label.
        '''
        with self.lock:
            return self.image

    def update_clock(self):
        '''
        Draw the clock and FPS on the NE corner of the screen.
        '''
        clock = datetime.now().isoformat()
        rate = self.frc.get_frame_rate()
        text = ' | '.join([clock, f'FPS: {rate:.2f}'])
        with self.lock:
            # Clear the text area by filling it with the background color
            text_area_width = 400
            text_area_height = 30
            cv2.rectangle(self.image,
                          (self.image.shape[1] - text_area_width, 0),
                          (self.image.shape[1], text_area_height),
                          self.background_color,
                          thickness=cv2.FILLED)

            # Draw the new text
            cv2.putText(self.image, text, (self.image.shape[1] - text_area_width + 5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255, 255), 1, cv2.LINE_AA)
        return

    def mk_image(self, image: np.ndarray = None, text: str = 'Powered by Listenzcc.') -> np.ndarray:
        '''
        Create an image with the given text and font size.
        '''
        if image is None:
            self.image = 100 + \
                np.zeros((self.height, self.width, 4), dtype=np.uint8)
        else:
            self.image = cv2.resize(image, (self.width, self.height))

        # Draw the text
        if text:
            cv2.putText(self.image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255, 255), 2, cv2.LINE_AA)

        return self.image


# %% ---- 2025-04-11 ------------------------
# Play ground


# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
