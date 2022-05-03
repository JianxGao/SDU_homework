import os
import librosa
from tensorflow import keras
from polycoherence import polycoherence
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft
import samplerate


def high_pass_filter(original_signal, order, fc, fs):
    b, a = signal.butter(N=order, Wn=2*fc/fs, btype='highpass')
    new_signal = signal.lfilter(b, a, original_signal)
    # print(a, b)
    return new_signal


def band_pass_filter(original_signal, order, fc1,fc2, fs):
    b, a = signal.butter(N=order, Wn=[2*fc1/fs,2*fc2/fs], btype='bandpass')
    new_signal = signal.lfilter(b, a, original_signal)
    # print(a,b)
    return new_signal


def low_pass_filter(original_signal, order, fc, fs):
    b, a = signal.butter(N=order, Wn=2*fc/fs, btype='lowpass')
    new_signal = signal.lfilter(b, a, original_signal)
    # print(a, b)
    return new_signal


def get_fft(dataset):
    N = len(dataset)
    X_data = dataset
    fft_value = np.abs(fft(X_data))
    fft_values = fft_value[0:N // 2]
    return fft_values


def plot_signal(audio_data, title=None):
    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(audio_data, linewidth=1)
    plt.grid()
    plt.title(title)
    plt.show()


def get_all_filenames(file_dir):
    all_files = [file for file in os.listdir(file_dir)]
    # print(all_files)
    return all_files


model = keras.models.load_model('h5_file/model_2.h5')

file_path = "../databases/stethoscope(wav)"
all_files = get_all_filenames(file_path)
for sub_path in all_files[-20:]:
    print(sub_path)
    audio_path = os.path.join(file_path, sub_path)
    audio_data, fs = librosa.load(audio_path, sr=None)  # load heart sound data
    # print("原始音频数据点数：",audio_data.shape,"采样率：", fs)

    audio_data = band_pass_filter(audio_data, 2, 25, 400, fs)
    down_sample_audio_data = samplerate.resample(audio_data.T, 1000 / fs, converter_type='sinc_best').T

    # print("现音频数据点数：", down_sample_audio_data.shape, "采样率：", 1000)
    dataset = np.zeros((1,256,256,1))
    freq1, fre2, bi_spectrum = polycoherence(down_sample_audio_data[-2000:], nfft=1024, fs=1000, norm=None, nperseg=256)
    bi_spectrum = np.array(abs(bi_spectrum))  # calculate bi_spectrum
    bi_spectrum = bi_spectrum.reshape((256, 256, 1))
    bi_spectrum = 255 * (bi_spectrum - np.min(bi_spectrum)) / (np.max(bi_spectrum) - np.min(bi_spectrum))
    dataset = np.vstack((dataset, np.array([bi_spectrum])))
    dataset = np.delete(dataset, 0, 0)

    # plot_signal(down_sample_audio_data, title=sub_path)
    res = model.predict(dataset)[0]
    print(res)
    print(np.argmax(res))
    print()
