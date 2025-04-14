"""
File: glfw_opengl.py
Author: Chuncheng Zhang
Date: 2025-04-13
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Display with GLFW and OpenGL

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-13 ------------------------
# Requirements and constants
from enum import Enum
import time
import glfw
import freetype
import numpy as np

from datetime import datetime
from collections import OrderedDict

from OpenGL.GL import *

from .logging import logger
from .fps_ruler import FPSRuler


# %% ---- 2025-04-13 ------------------------
# Function and class
class TextAnchor(Enum):
    '''
    NW ----- N ------ NE
    --------------------
    --------------------
    W ---- CENTER ---- E
    --------------------
    --------------------
    SW ----- S ------ SE
    '''
    CENTER = 0
    NW = 1
    NE = 2
    N = 3
    W = 4
    E = 5
    SW = 6
    SE = 7
    S = 8


class TextRenderer:
    def __init__(self, max_cache_size=1024):
        self.face = None
        self.characters = OrderedDict()  # 使用有序字典实现LRU缓存
        self.max_cache_size = max_cache_size  # 最大缓存字符数

    def load_font(self, font_path, size):
        """初始化字体"""
        self.face = freetype.Face(font_path)
        self.face.set_char_size(size << 6)
        logger.info(f'Using font: {font_path} ({size})')

    def load_char(self, char):
        """动态加载单个字符（支持中文字符）"""
        # 如果字符已在缓存中，移到最前面表示最近使用
        if char in self.characters:
            self.characters.move_to_end(char)
            return True

        # 如果缓存已满，移除最久未使用的字符
        if len(self.characters) >= self.max_cache_size:
            oldest_char = next(iter(self.characters))
            glDeleteTextures([self.characters[oldest_char]['texture']])
            del self.characters[oldest_char]
            logger.warning(
                f'Characters cache exceeds limit, removed: {oldest_char}')

        # 加载新字符
        self.face.load_char(char, freetype.FT_LOAD_RENDER |
                            freetype.FT_LOAD_TARGET_LIGHT)
        bitmap = self.face.glyph.bitmap

        # 将单通道位图转换为RGBA格式

        # -------------------------
        # It is Slow.
        # for i in range(bitmap.rows):
        #     for j in range(bitmap.width):
        #         value = bitmap.buffer[i * bitmap.width + j]
        #         rgba_data.extend([255, 255, 255, value])  # 白色+alpha
        # -------------------------

        buffer = np.array(bitmap.buffer, dtype=np.uint8).reshape(
            (bitmap.rows, bitmap.width))
        rgba_data = np.zeros((bitmap.rows, bitmap.width, 4), dtype=np.uint8)
        rgba_data[..., :3] = 255  # 设置RGB为白色
        rgba_data[..., 3] = buffer  # 设置Alpha通道
        rgba_data = rgba_data.flatten()

        # 生成纹理
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            bitmap.width, bitmap.rows,
            0, GL_RGBA, GL_UNSIGNED_BYTE,
            rgba_data
        )

        # 设置纹理参数
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # 存储字符信息
        self.characters[char] = {
            'texture': texture,
            'size': (bitmap.width, bitmap.rows),
            'bearing': (self.face.glyph.bitmap_left, self.face.glyph.bitmap_top),
            'advance': self.face.glyph.advance.x >> 6
        }

        # 将新字符移到最前面
        self.characters.move_to_end(char, last=False)
        logger.info(f'Loaded character: {char}, {self.characters[char]}')
        return True

    def bounding_box(self, text, scale=1.0):
        """计算文本的边界框"""
        width = 0
        height = 0
        for char in text:
            if char not in self.characters:
                self.load_char(char)

            ch = self.characters[char]
            width += ch['advance'] * scale
            height = max(height, ch['size'][1] * scale)

        return width, height

    def render_text(self, text, x, y, scale=1.0, color=(1.0, 1.0, 1.0, 1.0)):
        '''
        Draw the text at its SW corner.
        '''

        # 启用必要的OpenGL状态
        # glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        # 设置颜色（包含alpha通道）
        glColor4f(*color)

        # 获取视口尺寸用于坐标转换
        viewport = glGetIntegerv(GL_VIEWPORT)
        screen_width = viewport[2]
        screen_height = viewport[3]

        # 设置正交投影
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, screen_width, 0, screen_height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        for char in text:
            self.load_char(char)

            ch = self.characters[char]
            xpos = x + ch['bearing'][0] * scale
            ypos = y - (ch['size'][1] - ch['bearing'][1]) * scale

            w = ch['size'][0] * scale
            h = ch['size'][1] * scale

            # 绑定字符纹理
            glBindTexture(GL_TEXTURE_2D, ch['texture'])

            # 绘制字符
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(xpos, ypos + h)  # 左下角

            glTexCoord2f(1, 0)
            glVertex2f(xpos + w, ypos + h)  # 右下角

            glTexCoord2f(1, 1)
            glVertex2f(xpos + w, ypos)  # 右上角

            glTexCoord2f(0, 1)
            glVertex2f(xpos, ypos)  # 左上角
            glEnd()

            x += ch['advance'] * scale

        # 恢复矩阵状态
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        # 禁用状态
        glDisable(GL_TEXTURE_2D)
        # glDisable(GL_BLEND)


class GLFWWindow:
    # Monitor params (Read-only)
    width: int
    height: int
    refresh_rate: int

    # Window
    window = None

    # Options
    is_focused = True
    click_through = False

    # Addons
    text_renderer = TextRenderer()
    fps = FPSRuler()

    def __init__(self):
        pass

    def load_font(self, font_path: str, font_size: int = 48):
        self.text_renderer.load_font(font_path, font_size)
        self.font_path = font_path
        self.font_size = font_size
        return

    def on_focus_change(self, window, focused):
        self.is_focused = focused
        logger.info('Focus changed: {}'.format(
            'Got focus' if focused else 'Lost focus'))
        self.update_window_attributes()
        return

    def update_window_attributes(self):
        # 当窗口无焦点时自动启用点击穿透
        auto_click_through = not self.is_focused
        final_click_through = self.click_through or auto_click_through

        glfw.set_window_attrib(
            self.window,
            glfw.MOUSE_PASSTHROUGH,
            glfw.TRUE if final_click_through else glfw.FALSE
        )

        return

    def render_loop(self, key_callback: callable, main_render: callable):
        if not glfw.init():
            raise RuntimeError('Failed initialize GLFW')

        # 获取主显示器
        primary_monitor = glfw.get_primary_monitor()

        # 获取视频模式(包含分辨率信息)
        vid_mode = glfw.get_video_mode(primary_monitor)

        # 提取分辨率
        width, height = vid_mode.size
        refresh_rate = vid_mode.refresh_rate
        self.width = width
        self.height = height
        self.refresh_rate = refresh_rate
        logger.info(
            f'Using primary monitor: {width} x {height} ({refresh_rate} Hz)')

        # 配置窗口
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)  # 无边框
        glfw.window_hint(glfw.SAMPLES, 4)  # 抗锯齿
        glfw.window_hint(glfw.FLOATING, glfw.TRUE)  # 置顶窗口

        # 设置点击穿透
        # glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)

        # Leave out 1 pixel to prevent from crashing. But don't know why.
        window = glfw.create_window(
            width-1, height-1, 'OpenGL Wnd.', None, None)

        if not window:
            glfw.terminate()
            raise RuntimeError(f'Can not create window: {glfw.get_error()}')

        self.window = window

        # Make context and set callbacks.
        glfw.make_context_current(window)
        glfw.set_window_focus_callback(window, self.on_focus_change)
        glfw.set_key_callback(window, key_callback)
        # self.update_window_attributes()

        # 设置混合模式以实现透明度
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Main render
        fps = self.fps
        while not glfw.window_should_close(window):
            # 设置透明背景
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT)

            scale = 0.5
            color = (1.0, 1.0, 1.0, 1.0)

            text = f"GLFW ({glfw.__version__}) is Rendering at {width} x {height} ({refresh_rate} Hz)"
            self.draw_text(text, 0, 1.0, scale, TextAnchor.NW, color)

            text = '窗口获得焦点' if self.is_focused else '窗口失去焦点'
            self.draw_text(text, 0.5, 1.0, scale, TextAnchor.N, color)

            text = ' | '.join([
                datetime.now().isoformat(),
                f'FPS: {fps.get_fps():.2f}'
            ])
            self.draw_text(text, 1.0, 1.0, scale, TextAnchor.NE, color)

            main_render()

            glfw.swap_buffers(window)
            try:
                glfw.poll_events()
            except Exception as e:
                print(e)
                raise e
            fps.update()

        glfw.terminate()
        return

    def draw_rect(self, x, y, w, h, color=(1, 1, 1, 1)):
        '''
        Suppose the x, y is the SW corner of the rectangle.

        :param x, y, w, h: (0, 1) position and (0, 1) scale.
        '''
        if isinstance(color, float):
            color = (color, color, color, color)

        # x = x * 2.0 - 1.0
        # y = y * 2.0 - 1.0
        # w = w * 0.5
        # h = h * 0.5

        x = x * 2 - 1
        y = y * 2 - 1
        w *= 2
        h *= 2

        a = (x, y)
        b = (x, y+h)
        c = (x+w, y)
        d = (x+w, y+h)

        glBegin(GL_QUAD_STRIP)
        for e in [a, b, c, d]:
            glColor4f(*color)
            glVertex2f(*e)
        glEnd()
        return

    def draw_text(self, text, x, y, scale, anchor: TextAnchor, color=(1.0, 1.0, 1.0, 1.0)):
        '''
        The text is actually drawn by pixel units.

        :param x: (0, 1) position.
        :param y: (0, 1) position.
        '''
        if isinstance(color, float):
            color = (color, color, color, color)

        x = int(x * self.width)
        y = int(y * self.height)
        w, h = self.text_renderer.bounding_box(text, scale)

        if anchor == TextAnchor.SW:
            pass
        elif anchor == TextAnchor.SE:
            x -= w
        elif anchor == TextAnchor.S:
            x -= w // 2
        elif anchor == TextAnchor.NE:
            x -= w
            y -= h
        elif anchor == TextAnchor.NW:
            y -= h
        elif anchor == TextAnchor.N:
            x -= w // 2
            y -= h
        elif anchor == TextAnchor.CENTER:
            x -= w // 2
            y -= h // 2
        elif anchor == TextAnchor.W:
            y -= h // 2
        elif anchor == TextAnchor.E:
            y -= h // 2
            x -= w

        self.text_renderer.render_text(text, x, y, scale, color)
        return w, h


# %% ---- 2025-04-13 ------------------------
# Play ground

# %% ---- 2025-04-13 ------------------------
# Pending

# %% ---- 2025-04-13 ------------------------
# Pending
