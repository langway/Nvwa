#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import random
try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except:
        pass
except:
    pass
from PIL import ImageDraw, ImageFont, ImageFilter

#map:将str函数作用于后面序列的每一个元素
numbers = ''.join(map(str, range(10)))
chars = ''.join((numbers))

def create_validate_code(size=(80, 30), chars=chars, mode="RGB", bg_color=(255, 255, 255),
                         fg_color=(255, 0, 0), font_size=22, font_type="arial.ttf",
                         length=4, draw_points=True, point_chance = 4):
    """

    :rawParam size: 图片的大小，格式（宽，高），默认为(120, 30)
    :rawParam chars: 允许的字符集合，格式字符串
    :rawParam mode: 图片模式，默认为RGB
    :rawParam bg_color: 背景颜色，默认为白色
    :rawParam fg_color: 前景色，验证码字符颜色
    :rawParam font_size:验证码字体大小
    :rawParam font_type:验证码字体，默认为 Monaco.ttf
    :rawParam length:验证码字符个数
    :rawParam draw_points:是否画干扰点
    :rawParam point_chance:干扰点出现的概率，大小范围[0, 50]
    :return:
    """
    width, height = size
    img = Image.new(mode, size, bg_color) # 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔

    def get_chars():
        """''生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_points():
        """''绘制干扰点"""
        chance = min(50, max(0, int(point_chance))) # 大小限制在[0, 50]

        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """''绘制验证码字符"""
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 14),
                    strs, font=font, fill=fg_color)

        return strs

    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500, 0.001,
              float(random.randint(1, 2)) / 500]
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

    return img, strs
