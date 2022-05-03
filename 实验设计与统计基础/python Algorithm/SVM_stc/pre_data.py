from dsp_func import *
import pandas as pd


def get_strdata(dataset, index):
    data = [[] for i in range(dataset.shape[0])]
    for i in range(dataset.shape[0]):
        data[i] = np.array(dataset[i][index][1:-1].split(','))
        data[i] = data[i].astype(np.float64)
        # 截取数据
        # data[i] = data[i][-141:-1]
    return data


def get_intdata(dataset, index):
    num_data = [[] for i in range(dataset.shape[0])]
    for i in range(dataset.shape[0]):
        num_data[i] = np.array(int(dataset[i][index]))
    return num_data


def get_data(sport):
    acc_x = get_strdata(sport, 0)
    acc_y = get_strdata(sport, 1)
    acc_z = get_strdata(sport, 2)
    gry_x = get_strdata(sport, 3)
    gry_y = get_strdata(sport, 4)
    gry_z = get_strdata(sport, 5)
    # gender = get_intdata(sport, 6)
    # weight = get_intdata(sport, 7)
    # height = get_intdata(sport, 8)
    # times_a = get_strdata(sport, 9)
    # times_g = get_strdata(sport, 10)
    dataset = [[]for i in range(len(acc_x))]
    for i in range(len(acc_x)):
        #  data
        dataset[i].append(acc_x[i])
        dataset[i].append(acc_y[i])
        dataset[i].append(acc_z[i])
        dataset[i].append(gry_x[i])
        dataset[i].append(gry_y[i])
        dataset[i].append(gry_z[i])
        # dataset[i].append(gender[i])
        # dataset[i].append(weight[i])
        # dataset[i].append(height[i])
        #  label
    return np.array(dataset)


def remove_noise(data):
    return butter_filter(data)


def seperate_gravity_body(mixed_data):
    mixed_data = remove_noise(mixed_data)
    body_data = get_body(mixed_data)
    gravity_data = get_gravity(mixed_data)
    return body_data, gravity_data, mixed_data


# 单个数据
def split_data(data):
    N = 2 * (len(data[1]) // 128) - 1
    dataset = [np.copy(data) for i in range(N)]
    for i in range(N):
        for j in range(6):
            dataset[i][j] = np.array(data[j][i * 64:(i + 2) * 64])
    return np.array(dataset)


def get_spilt_data(data):
    body, gravity, total_data = seperate_gravity_body(data)
    body_dataset = split_data(body)
    gravity_dataset = split_data(gravity)
    total_dataset = split_data(total_data)
    return body_dataset, gravity_dataset, total_dataset


def get_initial(name):
    return get_data(pd.read_csv('ios_data/{}.csv'.format(name)).values)


def get_all_data(keep):
    dataset = [[[0, 0], [0], [0], [0], [0], [
        0], [0, 0], [0], [0], [0], [0], [0]]]
    total_dataset = [[[0, 0], [0], [0], [0], [0], [0]]]
    for i in range(len(keep)):
        data = keep[i]
        # 滤波滤除重力, 分别切割数据，50%的overlap
        body_data, gravity_data, total_data = get_spilt_data(data)
        cat_data = np.concatenate((body_data, gravity_data), axis=1)
        dataset = np.concatenate((dataset, cat_data), axis=0)
        # 切割重力和身体数据没有分离的数据
        total_dataset = np.concatenate((total_dataset, total_data), axis=0)
    body_and_gravity_dataset = dataset[1:]
    total_dataset = total_dataset[1:]
    return body_and_gravity_dataset, total_dataset
