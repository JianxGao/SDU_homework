import numpy as np
from PIL import Image


def show_image(im):
    im = im.resize((240, 240), Image.ANTIALIAS)
    with open('/dev/fb1', 'wb') as f:
        img = np.asarray(im)
        pix = np.zeros((240, 240, 2), dtype=np.uint8)
        pix[..., [1]] = np.add(np.bitwise_and(
            img[..., [0]], 0xF8), np.right_shift(img[..., [1]], 5))
        pix[..., [0]] = np.add(np.bitwise_and(np.left_shift(
            img[..., [1]], 3), 0xE0), np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tobytes()
        f.write(pix)


# Show the init image as fast as possible
im_init = Image.open('/home/pi/Desktop/material/init.png')
show_image(im_init)
im_AS = Image.open('/home/pi/Desktop/material/AS.png')
im_MR = Image.open('/home/pi/Desktop/material/MR.png')
im_MS = Image.open('/home/pi/Desktop/material/MS.png')
im_MVP = Image.open('/home/pi/Desktop/material/MVP.png')
im_wait = Image.open('/home/pi/Desktop/material/wait.png')
im_taking = Image.open('/home/pi/Desktop/material/taking.png')
im_normal = Image.open('/home/pi/Desktop/material/normal.png')
im_abnormal = Image.open('/home/pi/Desktop/material/abnormal.png')
im_welcome = Image.open('/home/pi/Desktop/material/welcome.png')
im_testing = Image.open('/home/pi/Desktop/material/testing.png')

import os
import samplerate
import tensorflow as tf
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt
from polycoherence import polycoherence
# import tflite_runtime.interpreter as tflite
import time
import RPi.GPIO as GPIO



def band_pass_filter(original_signal, order, fc1, fc2, fs):
    b, a = signal.butter(
        N=order, Wn=[2 * fc1 / fs, 2 * fc2 / fs], btype='bandpass')
    new_signal = signal.lfilter(b, a, original_signal)
    return new_signal



def plot_signal(audio_data, title=None):
    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(audio_data, linewidth=1)
    plt.grid()
    plt.savefig('/home/pi/Desktop/material/hs_data/hs_img.jpg')


RST_PIN = 25
CS_PIN = 8
DC_PIN = 24

KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13

KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


show_image(im_welcome)

print('begin')
dataset = np.ones((1, 256, 256, 1))
dataset = dataset.astype('float32')
while 1:
    
    # If you press key1 and then you pull up
    if not GPIO.input(KEY_PRESS_PIN):
        show_image(im_welcome)
    if not GPIO.input(KEY1_PIN):
        show_image(im_taking)
        os.system('arecord --format S32_LE --rate 2000 -c 2 -d 10 /home/pi/Desktop/sounds/test.wav')
        audio_path = '/home/pi/Desktop/sounds/test.wav'
        show_image(im_wait)
        audio_data, fs = sf.read(audio_path)
        audio_data = (audio_data[:, 0] + audio_data[:, 1]) / 2
        # print("原始音频数据点数：", audio_data.shape, "采样率：", fs)
        audio_data = band_pass_filter(audio_data, 2, 25, 400, fs)
        down_sample_audio_data = samplerate.resample(
            audio_data.T, 1000 / fs, converter_type='sinc_best').T
        down_sample_audio_data = down_sample_audio_data / np.max(np.abs(down_sample_audio_data))
        # print("现音频数据点数：", down_sample_audio_data.shape, "采样率：", 1000)
        plot_signal(down_sample_audio_data, title=audio_path)
        im = Image.open('/home/pi/Desktop/material/hs_data/hs_img.jpg')
        show_image(im)

        
        freq1, fre2, bi_spectrum = polycoherence(
            down_sample_audio_data[-2500:], nfft=1024, fs=1000, norm=None, nperseg=256)
        bi_spectrum = np.array(abs(bi_spectrum))  # calculate bi_spectrum
        bi_spectrum = bi_spectrum.reshape((256, 256, 1))
        bi_spectrum = 255 * (bi_spectrum - np.min(bi_spectrum)) / \
            (np.max(bi_spectrum) - np.min(bi_spectrum))
        dataset = np.vstack((dataset, np.array([bi_spectrum])))
        dataset = np.delete(dataset, 0, 0)
        dataset = dataset.astype('float32')
    if not GPIO.input(KEY2_PIN):
        show_image(im_testing)
        # Load the TFLite model and allocate tensors.
        # interpreter = tflite.Interpreter(model_path='model.tflite')
        interpreter2 = tf.lite.Interpreter(model_path='/home/pi/Desktop/material/normal_abnormal.tflite')

        interpreter2.allocate_tensors()
        # Get input and output tensors.
        input_details = interpreter2.get_input_details()
        output_details = interpreter2.get_output_details()
        # Test the model on random input data.
        input_shape = input_details[0]['shape']
        interpreter2.set_tensor(input_details[0]['index'], dataset)
        interpreter2.invoke()
        output_data = interpreter2.get_tensor(output_details[0]['index'])[0]
        print(output_data)
        print(np.argmax(output_data))
        print()

        if np.argmax(output_data) == 0:
            show_image(im_normal)
        else:
            show_image(im_abnormal)
    if not GPIO.input(KEY3_PIN):
        show_image(im_testing)
        # Load the TFLite model and allocate tensors.
        # interpreter = tflite.Interpreter(model_path='model.tflite')
        interpreter4 = tf.lite.Interpreter(model_path='/home/pi/Desktop/material/four_categories.tflite')
        interpreter4.allocate_tensors()
        # Get input and output tensors.
        input_details4 = interpreter4.get_input_details()
        output_details4 = interpreter4.get_output_details()
        # Test the model on random input data.
        input_shape = input_details4[0]['shape']
        interpreter4.set_tensor(input_details4[0]['index'], dataset)
        interpreter4.invoke()
        output_data = interpreter4.get_tensor(output_details4[0]['index'])[0]
        print(output_data)
        print(np.argmax(output_data))
        print()
        if np.argmax(output_data) == 0:
            show_image(im_AS)
        elif np.argmax(output_data) == 1:
            show_image(im_MS)
        elif np.argmax(output_data) == 2:
            show_image(im_MR)
        elif np.argmax(output_data) == 3:
            show_image(im_MVP)
