import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate  # 滤波,插值
from scipy.fftpack import fft


# 分离地心引力和身体运动
def get_body(data):
    newdata = np.copy(data)
    b, a = signal.butter(3, 0.012, 'highpass')
    for i in range(3):
        newdata[i] = signal.lfilter(b, a, data[i])  # data为要过滤的信号
    return newdata


def get_gravity(data):
    newdata = np.copy(data)
    b, a = signal.butter(3, 0.012, 'lowpass')
    for i in range(3):
        newdata[i] = signal.lfilter(b, a, data[i])  # data为要过滤的信号
    return newdata


def butter_filter(data):
    newdata = np.copy(data)
    b, a = signal.butter(3, 0.8, 'lowpass')
    for i in range(6):
        newdata[i] = signal.lfilter(b, a, data[i])  # data为要过滤的信号
    return newdata


def median_filter(data):
    newdata = np.copy(data)
    for i in range(6):
        newdata[i] = signal.medfilt(data[i], 3)
    return newdata


# 获取fft数据，已有格式
def get_fft(dataset):
    # 对每一个数据做FFT
    fft_values = np.copy(dataset)
    for i in range(dataset.shape[0]):
        # 对每个方向做FFT
        for j in range(dataset.shape[1]):
            N = len(dataset[i][j])  # 信号的长度
            X_data = dataset[i][j]
            # 傅里叶变换（归一化）
            fft_value = np.abs(fft(X_data)) / N
            fft_values[i][j] = fft_value[0:N // 2]
    return fft_values


# FFT变换  画图  仅供自己研究使用
def draw_fft(x_data):
    X1 = np.arange(len(x_data[0]))
    X2 = np.arange(len(x_data[3]))
    fig = plt.figure(figsize=(10, 6))
    # 三轴加速度
    for groupidx in range(len(x_data) - 4):
        # 信号的长度
        N = len(x_data[groupidx])
        # 傅里叶变换（归一化）
        fft_value = np.abs(fft(x_data[groupidx])) / N
        ax = fig.add_subplot(2, 3, groupidx + 1)
        # ax.plot(X1, fft_value, label="initial")
        ax.plot(X1[0:N // 2], fft_value[0:N // 2], label='normalization')
        ax.legend()
    for groupidx in range(len(x_data) - 4, len(x_data) - 1):
        # 信号的长度
        N = len(x_data[groupidx])
        # 傅里叶变换（归一化）
        fft_value = np.abs(fft(x_data[groupidx])) / N
        ax = fig.add_subplot(2, 3, groupidx + 1)
        # ax.plot(X2, fft_value, label="initial")
        ax.plot(X2[0:N // 2], fft_value[0:N // 2], label='normalization')
        ax.legend()
    plt.show()
