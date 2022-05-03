from util.extract_feature import *


if __name__ == '__main__':
    sports = dict(keep=0, squat=1, kaihetiao=2, high_leg_lift=3, squat_jump=4)
    all_dataset = np.zeros([1, 37])
    for key, value in sports.items():
        dataset = get_all_dataset(key, value)
        all_dataset = np.concatenate((all_dataset, dataset), axis=0)
        print(dataset.shape)
    all_dataset = pd.DataFrame(all_dataset[1:])
    all_dataset.to_csv('dataset_lll.csv', index=False)
