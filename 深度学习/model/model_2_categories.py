from tensorflow import keras


def build_model():
    inputdata = keras.Input(shape=(256, 256, 1))

    final = keras.layers.Conv2D(64, (3, 3), padding="same",activation='relu')(inputdata)
    final = keras.layers.BatchNormalization()(final)
    final = keras.layers.ReLU()(final)
    final = keras.layers.MaxPooling2D((2, 2), strides=(2, 2))(final)

    final = keras.layers.Conv2D(32, (3, 3), padding="same",activation='relu')(final)
    final = keras.layers.BatchNormalization()(final)
    final = keras.layers.ReLU()(final)
    final = keras.layers.MaxPooling2D((2, 2), strides=(2, 2))(final)

    final = keras.layers.Conv2D(16, (3, 3), padding="same",activation='relu')(final)
    final = keras.layers.BatchNormalization()(final)
    final = keras.layers.ReLU()(final)
    final = keras.layers.MaxPooling2D((2, 2), strides=(2, 2))(final)

    final = keras.layers.Conv2D(32, (3, 3), padding="same",activation='relu')(final)
    final = keras.layers.BatchNormalization()(final)
    final = keras.layers.ReLU()(final)

    final = keras.layers.Flatten()(final)
    final = keras.layers.Dense(2)(final)
    # final = keras.layers.BatchNormalization()(final)
    final = keras.layers.Softmax()(final)

    model = keras.Model(inputs=inputdata, outputs=final)
    optimizer = keras.optimizers.Adam(
        lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model

model = build_model()