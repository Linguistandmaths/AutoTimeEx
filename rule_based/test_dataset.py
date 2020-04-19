import os
import csv

from tqdm import tqdm


# class for downloading dataset

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

# get results


# write result to csv-files
with open(r'D:\anast\Documents\практ прога\1.csv', 'w', encoding='utf-8', newline='') as task1:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(task1, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        writer.writerow(row['predicted_tag'])


# evalute result
class Evaluator:
    """ Класс для оценки качества извлечения временных выражений """

    def __init__(self):
        self._predicted_files_dir = ''
        self._predicted_files = sorted(os.listdir(self._predicted_files_dir))

    def evaluate(self) -> str:
        """ Оценка качества извлечения временных выражений
        :return: метрики: precision, recall, F-1 score для каждого класса отдельно и для всех усреднённые
        """
        preds, targets = self._load_predictons()
        report = classification_report(y_true=targets, y_pred=preds)
        return report

    def _load_predictons(self):
        """ Загружает targets и predictions из заранее сформированных csv файлов
        :return: predictions, targets
        """
        preds = []
        targets = []
        for predicted_file in self._predicted_files:
            with open(os.path.join(self._predicted_files_dir, predicted_file), 'r') as predicted_file:
                reader = csv.DictReader(predicted_file)
                preds_from_file = []
                targets_from_file = []
                for row in reader:
                    preds_from_file.append(row['predicted_tag'])
                    targets_from_file.append(row['tag'])
                preds.append(preds_from_file)
                targets.append(targets_from_file)
        return preds, targets


if __name__ == '__main__':
    path_to_data_dir = '/Users/anast/PycharmProjects/AutoTimeEx2.0/dataset/train'
    dataset_loader = DatasetLoader(path_to_data_dir)
    # сохраняем в sentences набор тестовых данных
    sentences = dataset_loader.load_dataset()
    print('Loaded {} sentences'.format(str(len(sentences))))

    evaluator = Evaluator()
    report = evaluator.evaluate()
    print(report)

