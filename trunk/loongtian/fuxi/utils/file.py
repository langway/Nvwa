#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from os.path import exists, normpath, join, splitext
from os import makedirs
import PIL.Image
from PIL.ImageFile import Parser
from flask import request, Response, session
import time
from werkzeug.utils import secure_filename
from loongtian.fuxi import app
from loongtian.fuxi.conf.config import SITE_PATH
from loongtian.fuxi.utils.gateway import getIpAddress


def getFilePath(file_name=None, type='users', obj_id='0'):
    """
    生成用户资源对应的文件名和绝对路径
    文件名规则：根据类型设计， type=user时文件名为用户id
    :rawParam：file_name 原始文件名, type 上传头像类型也是目录名, obj_id对象id（需要id生成名字时用）
    :return：文件名，存储目录名，存储目录名路径+文件名
    example：('141832183000.bmp', 'D:\susers', 'D:\susers\141832183000.bmp')
    """
    if file_name:
        res = file_name.split('.')
        suffix = res[len(res)-1].lower()
        # 判断是否是支持的图片，否则返回None
        if suffix in ['jpg', 'jpeg', 'png', 'bmp']:
            cache = normpath(join(SITE_PATH, type))
            f_name = None
            if type == 'users':
                f_name = '%s%s' % (obj_id, splitext(file_name)[1])

            path = normpath(cache)
            return f_name, path, normpath(join(path, f_name))
        else:
            return None
    else:
        return None

@app.route('/upload/image', methods=['POST'])
def uploadImageFile():
    """
    接收js上传的图片
    """
    if request.method == 'POST':
        files = request.files.get('jUploaderFile', None)
        try:
            mine = session['user']
        except:
            return Response({'error': True, 'file_name': '用户未登陆！'})
        if files:
            # 在此处根据URL映射决定存储位置
            try:
                path_name = getFilePath(files.filename, 'users', mine['id'])
                if not exists(path_name[1]):
                    makedirs(path_name[1])
                fname = secure_filename(path_name[0])     #获取一个安全的文件名，且仅仅支持ascii字符；
                files.save(os.path.join(path_name[1], fname))

                json_r = json.dumps({'success': True, 'file_name': path_name[0]})
            except Exception as e:
                json_r = json.dumps({'error': True, 'file_name': ''})
            return Response(json_r)
        else:
            json_r = json.dumps({'error': True, 'file_name': ''})
            return Response(json_r)
    return Response({'error': True, 'file_name': ''})


@app.route('/upload/repics', methods=['POST'])
def uploadImageFilesCut():
    """
    对js上传的图片进行剪切
    """
    if request.method == 'POST':
        if 'imgtype' in request.form:
            img_type = request.form.get('imgtype', '')
            # 剪切的信息{'x':c.x,'y':c.y,'x2':c.x2,'y2':c.y2,'w':c.w,'h':c.h,'path':'已上传的图片路径', 'width':边框宽度，'height'：边框高度}
            imgs = request.form.get('img_info')
            img_list = []
            nums = request.form.getlist('num[]')
            img_info = eval(imgs)
            for num in nums:
                try:
                    num = eval(num)
                    img_name = img_info['path'].split('/')
                    img_name_src = img_name[-1]
                    img_path = normpath(join(SITE_PATH, 'users' , img_name_src))
                    tmp = Image.open(img_path)
                    tmp_new = clipResizeImage(tmp, int(num['width']), int(num['height']), str(img_info))  # 尺寸为图片显示区大小
                    tmp_new = resizeImage(tmp_new, int(num['width1']), int(num['height1']))
                    img_path = img_path.split('.')[0] + '_' + str(num['width1']) + 'x' + str(num['height1']) + '.' + img_path.split('.')[1]
                    tmp_new.save(img_path, quality=100)
                    img_name_r = img_info['path']
                    img_list.append(img_name_r)
                except Exception as e:
                    img_name_r = 500
                    img_list.append(img_name_r)
            img_list = json.dumps(img_list)
            return Response(img_list)

    return Response({'error': True, 'file_name': ''})

def resizeImage(ori_img=None, dst_w=0, dst_h=0):
    """
    等比例缩放图像[仅缩小原图像]
    如果缩小图像的同时没有其他操作，可以使用thumbnail()函数代替
    方法：
    im.thumbnail((192, 192), Image.ANTIALIAS)
    """
    ori_w, ori_h = ori_img.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    return ori_img.resize((newWidth, newHeight), Image.ANTIALIAS)

def clipResizeImage(ori_img=None, dst_w=0, dst_h=0, img_info=''):
    """
    裁剪并缩放图像
    """
    img_info = eval(img_info)
    ori_w, ori_h = ori_img.size
    dst_w = img_info['x2']
    dst_h = img_info['y2']
    widthRatio = heightRatio = None
    ratio = 1
    if ori_w >= ori_h:
        ratio = float(ori_w)/dst_w
    elif ori_w < ori_h:
        ratio = float(ori_h)/dst_h
    if ori_w < dst_w and ori_h < dst_h:
        ratio = 1
    x = int(img_info['x']*ratio)
    y = int(img_info['y']*ratio)
    widthRatio = int(img_info['w']*ratio)
    heightRatio = int(img_info['h']*ratio)
    if ori_h < heightRatio or ori_w < widthRatio:
        if ori_h < ori_w:
            ratio_s = ori_h/(heightRatio+0.0)
        else:
            ratio_s = ori_w/(widthRatio+0.0)
        x = int(x*ratio_s)
        y = int(y*ratio_s)
        widthRatio = int(ratio_s * widthRatio)
        if widthRatio > ori_w:
            widthRatio = ori_w
        if heightRatio > ori_h:
            heightRatio = int(ratio_s * heightRatio)
    if x < 0: x = 0
    if y < 0: y = 0
    box = (x, y, widthRatio + x, heightRatio + y)
    # 从图的(x, y)坐标开始截，截到(width + x, height + y)坐标处所包围的图像区域
    newIm = ori_img.crop(box)
    return newIm.resize((widthRatio, heightRatio), Image.ANTIALIAS)