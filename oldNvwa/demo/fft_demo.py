#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    fft_demo 
Author:   Liuyl 
DateTime: 2014/9/15 11:08 
UpdateLog:
1、Liuyl 2014/9/15 Create this File.

fft_demo
>>> print("No Test")
No Test
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import wave
__author__ = 'Liuyl'


def fft_combine(freqs, n, loops=1):
    length = len(freqs) * loops
    data = np.zeros(length)
    index = loops * np.arange(0, length, 1.0) / length * (2 * np.pi)
    for k, p in enumerate(freqs[:n]):
        if k != 0: p *= 2  # 除去直流成分之外，其余的系数都*2
        data += np.real(p) * np.cos(k * index)  # 余弦成分的系数为实数部
        data -= np.imag(p) * np.sin(k * index)  # 正弦成分的系数为负的虚数部
    return index, data


def test1():
    # 最先确定的是采样率，采样率确定意味着两方面的事情。
    # 1.时间轴：确定每隔多久对信号采样一次，即离散化的时域轴的间隔确定，但是总长没定。
    # 2.频率轴：的总长确定了，为采样率的一半，但是间隔没定。
    Fs = 100
    T_interval = 1 / Fs
    Freq_max = Fs / 2

    N = 1024
    t = np.arange(0, N - 1) * T_interval
    freq = np.linspace(0, Freq_max, N / 2 + 1)

    sig = np.sin(1 * 2 * np.pi * t) + 2 * np.sin(2 * 2 * np.pi * t) + 0.5 * np.cos(5 * 2 * np.pi * t)
    fft_sig = np.fft.rfft(sig, N) / N
    print(fft_sig)
    # 画出时间域的幅度图
    fig = plt.figure('Fourier')
    plt.subplot(211)
    plt.plot(t, sig, label="$sin(100\pi*t)+sin(200\pi*t)+sin(500\pi*t)$")
    plt.title(u'Original Signal')
    plt.xlabel(u'Time(s)')
    plt.ylabel(u'Volt')
    plt.legend()


    # 画出频域图,你会发现你的横坐标无从下手？虽然你懂了后面的东西后可以返回来解决，但是现在就非常迷惑。现在只能原封不懂的画出频率图
    plt.subplot(212)

    plt.plot(freq, 2 * np.abs(fft_sig), 'red', label='Frequency')  # 如果用db作单位则20*np.log10(2*np.abs(fft_sig))
    plt.title(u'Frenquency Spectrum')
    plt.xlabel(u'Frequency(Hz)')
    plt.ylabel(u'Proportion')
    plt.legend()
    plt.show()

    # plt.subplot(313)
    # for i in [0, 1, 3, 5, 7, 9]:
    # index, dataDict = fft_combine(fy, i + 1, 2)  # 计算两个周期的合成波形
    #     plt.plot(dataDict, label="N=%s" % i)
    # plt.legend()
    # plt.title("partial Fourier series of triangle wave")
    plt.show()


def test2():
    sampling_rate = 8000
    fft_size = 512
    t = np.arange(0, 1.0, 1.0 / sampling_rate)
    x = np.sin(2 * np.pi * 156.25 * t) + 2 * np.sin(2 * np.pi * 234.375 * t)
    # x = np.sin(2 * np.pi * 200 * t) + 2 * np.sin(2 * np.pi * 400 * t)
    xs = x[:fft_size] * signal.hann(fft_size, sym=0) * 2
    xf = np.fft.rfft(xs) / fft_size
    freqs = np.linspace(0, sampling_rate / 2, fft_size / 2 + 1)
    xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    plt.figure(figsize=(8, 4))
    plt.subplot(211)
    plt.plot(t[:fft_size], xs)
    plt.xlabel(u"时间(秒)")
    plt.title(u"156.25Hz和234.375Hz的波形和频谱")
    plt.subplot(212)
    plt.plot(freqs, xfp)
    plt.xlabel(u"频率(Hz)")
    plt.subplots_adjust(hspace=0.4)
    plt.show()


def test3():
    sampling_rate = 8000
    fft_size = 512
    t = np.arange(0, 1.0, 1.0 / sampling_rate)
    x = np.sin(2 * np.pi * 200 * t) + 2 * np.sin(2 * np.pi * 300 * t)

    xs = x[:fft_size]
    ys = xs * signal.hann(fft_size, sym=0)
    plt.plot(np.hstack([ys, ys, ys]))
    plt.show()
    xf = np.fft.rfft(xs) / fft_size
    yf = np.fft.rfft(ys) / fft_size
    freqs = np.linspace(0, sampling_rate / 2, fft_size / 2 + 1)
    xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    yfp = 20 * np.log10(np.clip(np.abs(yf), 1e-20, 1e100))
    plt.figure(figsize=(8, 4))
    plt.title(u"200Hz和300Hz的波形和频谱")
    plt.plot(freqs, xfp, label=u"矩形窗")
    plt.plot(freqs, yfp, label=u"hann窗")
    plt.legend()
    plt.xlabel(u"频率(Hz)")

    a = plt.axes([.4, .2, .4, .4])
    a.plot(freqs, xfp, label=u"矩形窗")
    a.plot(freqs, yfp, label=u"hann窗")
    a.set_xlim(100, 400)
    a.set_ylim(-40, 0)
    plt.show()


def test4():
    # 打开WAV文档
    f = wave.open(r"c:\WINDOWS\Media\ding.wav", "rb")
    
    # 读取格式信息
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    
    # 读取波形数据
    str_data = f.readframes(nframes)
    f.close()
    
    #将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    time = np.arange(0, nframes) * (1.0 / framerate)
    
    # 绘制波形
    plt.subplot(211) 
    plt.plot(time, wave_data[0])
    plt.subplot(212) 
    plt.plot(time, wave_data[1], c="g")
    plt.xlabel("recordTime (seconds)")
    plt.show()

if __name__ == '__main__':
    # http://www.linuxeden.com/html/news/20140607/152446.html
    # http://www.open-open.com/news/view/1b9ad6e
    test4()