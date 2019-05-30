#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except:
        pass
except:
    pass

import subprocess
import time
import errors
import util
import shlex
import os

USE_LOCAL=False # 是否使用本地提供的tesseract程序

if USE_LOCAL:
    tesseract_exe_path = os.path.split(os.path.realpath(__file__))[0] + "\\tesseract"  # Name of executable to be called at command line
    tessdata_dir_config=None
else:
    tesseract_setup_path= "D:\\Program Files (x86)\\Tesseract-OCR"
    tesseract_exe_path= "{0}\\tesseract".format(tesseract_setup_path)
    tessdata_dir_config = '--tessdata-dir "{0}\\tessdata"'.format(tesseract_setup_path)
# Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# It's important to add double quotes around the dir path.

scratch_image_name = "temp.bmp"  # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp"  # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation


def call_tesseract(input_filename, output_filename, lang=None, boxes=False,
                  config=tessdata_dir_config):
    """Calls external tesseract.exe on input file (restrictions on types),
    outputting output_filename+'txt'"""
    command = [tesseract_exe_path, input_filename, output_filename]
    if lang is not None:
        command += ['-l', lang]

    if boxes:
        command += ['batch.nochop', 'makebox']

    if config:
        command += shlex.split(config)

    proc = subprocess.Popen(command,shell=True)
    retcode = proc.wait()
    if retcode != 0:
        errors.check_for_errors()


def image_to_string(im,
                    record_time=False ,
                    cleanup=cleanup_scratch_flag, lang=None, boxes=False,
                  config=tessdata_dir_config):
    """Converts im to file, applies tesseract, and fetches resulting text.
    If cleanup=True, delete scratch files after operation."""
    if record_time:
        start = time.time()


    try:
        util.image_to_scratch(im, scratch_image_name)
        call_tesseract(scratch_image_name, scratch_text_name_root,lang,boxes,config)
        text = util.retrieve_text(scratch_text_name_root)
    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)

    if record_time:
        end = time.time()
        duration=end - start
        print ("duration: %f s" % (duration))

    return text


def image_file_to_string(filename,
                         record_time=False ,
                         cleanup=cleanup_scratch_flag,
                         graceful_errors=True, lang=None, boxes=False,
                         config=tessdata_dir_config):
    """Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
    converts to compatible format and then applies tesseract.  Fetches resulting text.
    If cleanup=True, delete scratch files after operation."""
    if record_time:
        start = time.time()

    use_image_to_string=False

    try:
        call_tesseract(filename, scratch_text_name_root,lang,boxes,config)
        text = util.retrieve_text(scratch_text_name_root)
    except errors.Tesser_General_Exception:
        if graceful_errors:
            im = Image.open(filename)
            text = image_to_string(im,False,cleanup,lang,boxes,config)
            use_image_to_string=True
        else:
            raise
    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)

    if record_time:
        end = time.time()
        duration=end - start
        print ("duration: %f s" % (duration))

    if graceful_errors and use_image_to_string:
        return text,use_image_to_string
    else:
        return text


if __name__ == '__main__':

    # filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\test.png"
    # text = image_file_to_string(filename,record_time=True)
    # print (text)
    #
    # filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\phototest.tif"
    # text = image_file_to_string(filename,record_time=True)
    # print (text)
    #
    # filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\fnord.tif"
    # try:
    #     text = image_file_to_string(filename, graceful_errors=False,record_time=True)
    #     print (text)
    # except errors.Tesser_General_Exception as ex:
    #     print ("fnord.tif is incompatible filetype.  Try graceful_errors=True")
    #     print (ex)
    #
    # text = image_file_to_string(filename, graceful_errors=True,record_time=True)
    # print ("fnord.tif contents:", text)
    #
    # filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\fonts_test.png"
    # text = image_file_to_string(filename, graceful_errors=True,record_time=True)
    # print (text)
    #
    # filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\test-european.jpg"
    # text = image_file_to_string(filename, graceful_errors=True,record_time=True)
    # print (text)

    filename = os.path.split(os.path.realpath(__file__))[0] + "\\pics\\grabed.png"
    text = image_file_to_string(filename, graceful_errors=True, record_time=True)
    print (text)
