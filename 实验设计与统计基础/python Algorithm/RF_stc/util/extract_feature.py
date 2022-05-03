"""
Data Structure：
          0      1      2
    body: acc_x, acc_y, acc_z
          3      4      5
    gyro: gyro_x, gyro_y, gyro_z
          6      7      8
    grav: g_x,   g_y,   g_z
          9      10     11
    gyro: gyr_x, gyro_y, gyro_z

"""
import time
from pre_data import *


def vision3(dataset1, dataset2, dataset3):
    fig = plt.figure(figsize=(10, 6))
    for groupidx in range(len(dataset1)):
        ax = fig.add_subplot(len(dataset1)/3, 3, groupidx + 1)
        ax.plot(dataset1[groupidx], label='body_data')
        ax.plot(dataset2[groupidx], label='gravity_data')
        ax.plot(dataset3[groupidx], label='total_data')
        ax.legend()
    plt.show()


def vision1(dataset1):
    fig = plt.figure(figsize=(10, 6))
    for groupidx in range(len(dataset1)):
        ax = fig.add_subplot((len(dataset1)/3), 3, groupidx + 1)
        ax.plot(dataset1[groupidx], label='data')
        # ax.plot(dataset2[groupidx], label='gravity_data')
        # ax.plot(dataset3[groupidx], label='total_data')
        ax.legend()
    plt.show()


def get_mad(data):
    # mad = b * np.median(np.abs(total_data - median))
    median = np.median(data)
    return np.median(np.abs(data-median))


def get_feature(data, total_data, fft_b_g, total_fft, label):
    length = data.shape[0]
    dataset = [[]for i in range(length)]
    for i in range(length):
    # ACC
        # acc_body
        for j in range(6):
            dataset[i].append(np.mean(data[i][j]))  # acc_body_mean
            dataset[i].append(np.std(data[i][j]))   # acc_body_std
            dataset[i].append(np.max(data[i][j]))   # acc_body_max
            dataset[i].append(np.min(data[i][j]))   # acc_body_min
            # dataset[i].append(get_mad(data[i][j]))  # acc_body_mad
            dataset[i].append(np.sum(np.square(data[i][j]))/len(data[i][j]))  # acc_body_energy
            # dataset[i].append(np.percentile(data[i][j], 75)-np.percentile(data[i][j], 25))  # acc_body_iqr

        # # acc_gravity
        # for j in range(6, 9):
        #     dataset[i].append(np.mean(data[i][j]))  # acc_gravity_mean
        #     dataset[i].append(np.std(data[i][j]))   # acc_gravity_std
        #     dataset[i].append(np.max(data[i][j]))   # acc_gravity_max
        #     dataset[i].append(np.min(data[i][j]))   # acc_gravity_min
        #     dataset[i].append(get_mad(data[i][j]))  # acc_gravity_mad
        #     dataset[i].append(np.sum(np.square(data[i][j])) / len(data[i][j]))  # acc_gravity_energy
        #     dataset[i].append(np.percentile(data[i][j], 75) - np.percentile(data[i][j], 25))  # acc_gravity_iqr
        #
        # # gyro
        # for j in range(4, 6):
        #     dataset[i].append(np.mean(data[i][j]))  # gyro_mean
        #     dataset[i].append(np.std(data[i][j]))   # gyro_std
        #     dataset[i].append(np.max(data[i][j]))   # gyro_max
        #     dataset[i].append(np.min(data[i][j]))   # gyro_min
        #     dataset[i].append(get_mad(data[i][j]))  # gyro_mad
        #     dataset[i].append(np.sum(np.square(data[i][j])) / len(data[i][j]))  # gyro_energy
        #     dataset[i].append(np.percentile(data[i][j], 75) - np.percentile(data[i][j], 25))  # gyro_iqr

        # # acc_total_data, gyro NO CHANGE!
        # for j in range(3):
        #     dataset[i].append(np.mean(total_data[i][j]))  # acc_total_data_mean
        #     dataset[i].append(np.std(total_data[i][j]))  # acc_total_data_std
        #     dataset[i].append(np.max(total_data[i][j]))  # acc_total_data_max
        #     dataset[i].append(np.min(total_data[i][j]))  # acc_total_data_min
        #     # dataset[i].append(get_mad(total_data[i][j]))  # acc_total_data_mad
        #     dataset[i].append(np.sum(np.square(total_data[i][j])) / len(total_data[i][j]))  # acc_total_data_energy
        #     # dataset[i].append(
        #     #     np.percentile(total_data[i][j], 75) - np.percentile(total_data[i][j], 25))  # acc_total_data_iqr

        # acc_body_correlation
        dataset[i].append(np.corrcoef(data[i][0], data[i][1])[0][1])
        dataset[i].append(np.corrcoef(data[i][1], data[i][2])[0][1])
        dataset[i].append(np.corrcoef(data[i][0], data[i][2])[0][1])

        # gyro_correlation
        dataset[i].append(np.corrcoef(data[i][3], data[i][4])[0][1])
        dataset[i].append(np.corrcoef(data[i][3], data[i][5])[0][1])
        dataset[i].append(np.corrcoef(data[i][4], data[i][5])[0][1])

        # # acc_gravity_correlation
        # dataset[i].append(np.corrcoef(data[i][6], data[i][7])[0][1])
        # dataset[i].append(np.corrcoef(data[i][6], data[i][8])[0][1])
        # dataset[i].append(np.corrcoef(data[i][7], data[i][8])[0][1])
        #
        # # acc_total_data_correlation
        # dataset[i].append(np.corrcoef(total_data[i][0], total_data[i][1])[0][1])
        # dataset[i].append(np.corrcoef(total_data[i][0], total_data[i][2])[0][1])
        # dataset[i].append(np.corrcoef(total_data[i][1], total_data[i][2])[0][1])

    # # FFT
    #     # fft_body
    #     for j in range(9):
    #         dataset[i].append(np.mean(fft_b_g[i][j]))  # fft_body_mean
    #         dataset[i].append(np.std(fft_b_g[i][j]))   # fft_body_std
    #         dataset[i].append(np.max(fft_b_g[i][j]))   # fft_body_max
    #         dataset[i].append(np.min(fft_b_g[i][j]))   # fft_body_min
    #         # dataset[i].append(get_mad(fft_b_g[i][j]))  # fft_body_mad
    #         dataset[i].append(np.sum(np.square(fft_b_g[i][j])) / len(fft_b_g[i][j]))  # fft_body_energy
    #         # dataset[i].append(np.percentile(fft_b_g[i][j], 75) - np.percentile(fft_b_g[i][j], 25))  # fft_body_iqr
    #     # fft_acc_body_correlation
    #     dataset[i].append(np.corrcoef(fft_b_g[i][0], fft_b_g[i][1])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][1], fft_b_g[i][2])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][0], fft_b_g[i][2])[0][1])
    #
    #     # fft_gyro_correlation
    #     dataset[i].append(np.corrcoef(fft_b_g[i][3], fft_b_g[i][4])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][3], fft_b_g[i][5])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][4], fft_b_g[i][5])[0][1])
    #
    #     # fft_acc_gravity_correlation
    #     dataset[i].append(np.corrcoef(fft_b_g[i][6], fft_b_g[i][7])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][6], fft_b_g[i][8])[0][1])
    #     dataset[i].append(np.corrcoef(fft_b_g[i][7], fft_b_g[i][8])[0][1])
    #
    #     # fft_acc_total_data_correlation
    #     dataset[i].append(np.corrcoef(total_fft[i][0], total_fft[i][1])[0][1])
    #     dataset[i].append(np.corrcoef(total_fft[i][0], total_fft[i][2])[0][1])
    #     dataset[i].append(np.corrcoef(total_fft[i][1], total_fft[i][2])[0][1])
        # # fft_gravity
        # for j in range(6, 9):
        #     dataset[i].append(np.mean(fft_b_g[i][j]))  # fft_gravity_mean
        #     dataset[i].append(np.std(fft_b_g[i][j]))   # fft_gravity_std
        #     dataset[i].append(np.max(fft_b_g[i][j]))   # fft_gravity_max
        #     dataset[i].append(np.min(fft_b_g[i][j]))   # fft_gravity_min
        #     dataset[i].append(get_mad(fft_b_g[i][j]))  # fft_gravity_mad
        #     dataset[i].append(np.sum(np.square(fft_b_g[i][j])) / len(fft_b_g[i][j]))  # fft_gravity_energy
        #     dataset[i].append(np.percentile(fft_b_g[i][j], 75) - np.percentile(fft_b_g[i][j], 25))  # fft_gravity_iqr
        # # fft_gyro
        # for j in range(3, 6):
        #     dataset[i].append(np.mean(fft_b_g[i][j]))  # fft_gyro_mean
        #     dataset[i].append(np.std(fft_b_g[i][j]))   # fft_gyro_std
        #     dataset[i].append(np.max(fft_b_g[i][j]))   # fft_gyro_max
        #     dataset[i].append(np.min(fft_b_g[i][j]))   # fft_gyro_min
        #     dataset[i].append(get_mad(fft_b_g[i][j]))  # fft_gyro_mad
        #     dataset[i].append(np.sum(np.square(fft_b_g[i][j])) / len(fft_b_g[i][j]))  # fft_gyro_energy
        #     dataset[i].append(np.percentile(fft_b_g[i][j], 75) - np.percentile(fft_b_g[i][j], 25))  # fft_gyro_iqr
        dataset[i].append(label)
    return np.array(dataset)


def calcute_time(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        take_time = time.time() - start_time
        print("Function '{0}' takes {1:.3f}s.".format(
            func.__name__, take_time))
        return f
    return wrapper


@calcute_time
def get_all_dataset(sports, label):
    body_and_gravity_dataset, total_dataset = get_all_data(get_initial(sports))
    # 检查数据是否正确
    # print(body_and_gravity_dataset.shape)
    # print(total_dataset.shape)
    # 快速傅立叶变换
    fft_body_and_gravity_dataset = get_fft(body_and_gravity_dataset)
    fft_total_dataset = get_fft(total_dataset)

    # # 检验
    # print("Single data's shape：")
    # # 重力和身体数据没有分离
    # print('\ttotal_dataset.shape:\t\t\t', total_dataset[0].shape)
    # # 重力和身体数据没有分离的FFT
    # print('\tfft_total_dataset.shape:\t\t', fft_total_dataset[0].shape)
    # # 重力和身体数据
    # print('\tbody_and_gravity_dataset.shape: ', body_and_gravity_dataset[0].shape)
    # # 重力和身体数据的FFT
    # print('\tfft_body_and_gravity_dataset.shape', fft_body_and_gravity_dataset[0].shape)

    # 画图检验
    # vision1(fft_body_and_gravity_dataset[0])
    # vision1(fft_total_dataset[0])
    # vision1(total_dataset[0])
    # vision3(total_dataset[0], body_and_gravity_dataset[0][:6],body_and_gravity_dataset[0][6:])

    # 特征提取
    dataset = get_feature(body_and_gravity_dataset,
                          total_dataset,
                          fft_body_and_gravity_dataset,
                          fft_total_dataset, label)
    return dataset


get_all_dataset('high_leg_lift', 0)