import os
import tensorflow as tf


def get_all_filenames(file_dir):
    all_files = [file for file in os.listdir(file_dir)]
    return all_files


all_files = get_all_filenames('h5_file')
for name in all_files:
    model = tf.keras.models.load_model('h5_file/{}'.format(name))
    # print(model.summary())
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    # Save the model
    with open('tflite_file/{}.tflite'.format(name[:-3]), 'wb') as f:
        f.write(tflite_model)


