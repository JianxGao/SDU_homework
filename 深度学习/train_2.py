import numpy as np
from model.model_2_categories import build_model
from extract_bispectrum import get_bi_spectrum


def cal_acc(label,prediction):
    num=0
    N = len(label)
    for i in range(len(label)):
        pred = np.argmax(prediction[i])
        if label[i]==pred:
            num+=1
    return num/N


def shuffle_data_label(data, label):
    state = np.random.get_state()
    np.random.shuffle(data)
    np.random.set_state(state)
    np.random.shuffle(label)
    return data,label


def generate_label(num=14000):
    label = []
    for j in range(2):
        for i in range(num):
            label.append(j)
    return np.array(label)


if __name__ == '__main__':
    np.random.seed(0)
    file_folder = 'databases/database_two_categories'
    class_name = ['n','abn']
    dataset = get_bi_spectrum(file_folder, class_name,14000)
    np.save('dataset28000',dataset)
    label = generate_label()
    img_data,label = shuffle_data_label(dataset,label)
    train_data = img_data[:25000,:,:]
    test_data = img_data[25000:,:,:]
    train_label = label[:25000]
    test_label = label[25000:]
    # print(train_data.shape)
    num_epochs = 600
    model = build_model()
    history = model.fit(train_data, train_label,
                        epochs=num_epochs,
                        batch_size=32,
                        # validation_split=0.2,
                        verbose=1)
    model.save('model/h5_file/model_2.h5')
    test_predictions = model.predict(test_data)
    np.save('result/result_4/pred',test_predictions)
    np.save('result/result_4/label',test_label)
    acc = cal_acc(test_label, test_predictions)
    print(acc)

