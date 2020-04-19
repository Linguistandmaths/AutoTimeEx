import os
import csv

from tqdm import tqdm


class DatasetLoader:

    def __init__(self, path_to_data_dir):
        self._path_to_data_dir = path_to_data_dir
        self._data_files = sorted(os.listdir(self._path_to_data_dir))


    def load_dataset(self):
        """
        загружает датасет из папки, путь к которой указывали в path_to_data_dir
        :return: список из
        """
        sentences = []
        for data_file in tqdm(self._data_files, desc='Loading data'):
            with open(os.path.join(self._path_to_data_dir, data_file), 'r') as data_f:
                reader = csv.DictReader(data_f)
                sentence = []
                for row in reader:
                    sentence.append((row['token'], row['tag']))
                sentences.append(sentence)
        return sentences


if __name__ == '__main__':
    path_to_data_dir = '/Users/anast/PycharmProjects/AutoTimeEx2.0/dataset/train'
    dataset_loader = DatasetLoader(path_to_data_dir)
    sentences = dataset_loader.load_dataset()
    print('Loaded {} sentences'.format(str(len(sentences))))
