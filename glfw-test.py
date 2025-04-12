import time
import glfw
import freetype
import numpy as np

from datetime import datetime
from threading import Thread
from collections import OrderedDict

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from util.fps_ruler import FPSRuler

fps = FPSRuler()


def performance_ruler():
    while True:
        print(f"FPS: {fps.get_fps()}")
        fps.update()
        time.sleep(1)


Thread(target=performance_ruler, daemon=True).start()


class TextRenderer:
    def __init__(self, max_cache_size=1024):
        self.face = None
        self.characters = OrderedDict()  # 使用有序字典实现LRU缓存
        self.max_cache_size = max_cache_size  # 最大缓存字符数

    def load_font(self, font_path, size):
        """初始化字体"""
        self.face = freetype.Face(font_path)
        self.face.set_char_size(size << 6)

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
        print('Loading character:', char, self.characters[char])
        return True

    def text_box(self, text, scale=1.0):
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
        # 启用必要的OpenGL状态
        glEnable(GL_BLEND)
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
        glDisable(GL_BLEND)


def sin(t):
    return np.sin(t*2*np.pi)


def cos(t):
    return np.cos(t*2*np.pi)


def key_callback(window, key, scancode, action, mods):
    """键盘事件回调函数"""
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        print("ESC键被按下，关闭窗口")
        glfw.set_window_should_close(window, True)
    elif action == glfw.PRESS:
        print(f"键 {key} 被按下")
    elif action == glfw.RELEASE:
        print(f"键 {key} 被释放")
    elif action == glfw.REPEAT:
        print(f"键 {key} 重复")


def main():
    # 初始化GLFW
    if not glfw.init():
        raise RuntimeError("无法初始化GLFW")

    # 获取主显示器
    primary_monitor = glfw.get_primary_monitor()

    # 获取视频模式(包含分辨率信息)
    vid_mode = glfw.get_video_mode(primary_monitor)

    # 提取分辨率
    width, height = vid_mode.size
    refresh_rate = vid_mode.refresh_rate
    print(width, height, refresh_rate)

    # 配置窗口
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)  # 无边框
    glfw.window_hint(glfw.SAMPLES, 4)  # 抗锯齿
    glfw.window_hint(glfw.FLOATING, glfw.TRUE)  # 置顶窗口

    window = glfw.create_window(width-1, height-1, "透明OpenGL窗口", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError(f'Can not create window: {glfw.get_error()}')

    # Make context and set key callback.
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # 创建文本渲染器
    text_renderer = TextRenderer()
    text_renderer.load_font("./font/msyh.ttc", 24)

    # 设置混合模式以实现透明度
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # 主渲染循环
    while not glfw.window_should_close(window):
        # 设置透明背景
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        text_renderer.render_text(
            "OpenGL is Rendering", 100, 100, 0.8, (0.2, 0.8, 0.5, 1.0))

        text_renderer.render_text(
            "中文字符", 0, 300, 0.8, (0.2, 0.8, 0.5, 1.0))

        clock = datetime.now().isoformat()
        rate = fps.get_fps()
        text = ' | '.join([clock, f'FPS: {rate:.2f}'])
        w, h = text_renderer.text_box(text, 0.8)
        text_renderer.render_text(
            text, width-w, height-h, 0.8, (1.0, 1.0, 1.0, 1.0))

        # 在这里添加你的渲染代码
        # 示例：绘制一个半透明三角形
        # Range is [-1, -1] -> [1, 1]
        t = time.time()
        d = t * 0.1
        glBegin(GL_TRIANGLES)
        glColor4f(1.0, 0.0, 0.0, 0.5)  # 红色，50%透明度
        glVertex2f(cos(d), sin(d))
        glColor4f(0.0, 1.0, 0.0, 0.5)  # 绿色，50%透明度
        glVertex2f(cos(d+1/3), sin(d+1/3))
        glColor4f(0.0, 0.0, 1.0, 0.5)  # 蓝色，50%透明度
        glVertex2f(cos(d+2/3), sin(d+2/3))
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()
        fps.update()

    glfw.terminate()


if __name__ == "__main__":
    main()
