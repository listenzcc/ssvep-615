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
import time
from datetime import datetime
from threading import Thread, RLock
import sys
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from .logging import logger
from .frame_rate_counter import FrameRateCounter

# Initialize the QApplication in the first place.
qapp = QApplication(sys.argv)

small_font = ImageFont.truetype("arial.ttf", 24)
large_font = ImageFont.truetype("arial.ttf", 64)

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
    background_color = (0, 0, 0, 0)  # RGBA

    def __init__(self, image: Image = None) -> None:
        super().__init__()
        self.lock = RLock()
        self.frc = FrameRateCounter(max_samples=100)
        self.mk_image(image)
        self.put_image()
        logger.info('ImageQtWindow initialized.')
        pass

    def put_image(self, image: Image = None):
        '''
        Put the image to the pixmap_label.
        '''
        if image:
            self.image = image
        with self.lock:
            image_qt = ImageQt(self.image)
        self.pixmap = QPixmap.fromImage(image_qt)
        self.pixmap_label.setPixmap(self.pixmap)
        return

    def get_image(self) -> Image:
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
        text_bbox = self.image_draw.textbbox((0, 0), text, font=small_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        with self.lock:
            self.image_draw.rectangle(
                (self.image.width - text_width - 10, 0, self.image.width, text_height + 10), fill=self.background_color)
            self.image_draw.text((self.image.width - 10, 0), text=text,
                                 fill=(255, 255, 255), font=small_font, anchor='rt')
        pass

    def mk_image(self, image: Image = None, text: str = 'Default image.') -> Image:
        '''
        Create an image with the given text and font size.
        '''
        if image is None:
            self.image = Image.new(
                'RGBA', (self.width, self.height), self.background_color)
            self.image_draw = ImageDraw.Draw(self.image)
        else:
            image = image.resize((self.width, self.height))
            self.image = image

        # Draw the text
        if text:
            font = small_font  # large_font
            self.image_draw.text((0, 0), text=text,
                                 fill=(255, 255, 255), font=font)

        return self.image


# %% ---- 2025-04-11 ------------------------
# Play ground


# %% ---- 2025-04-11 ------------------------
# Pending


# %% ---- 2025-04-11 ------------------------
# Pending
