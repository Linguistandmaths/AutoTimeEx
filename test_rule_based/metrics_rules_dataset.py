import os
import csv
from seqeval.metrics import classification_report
from tqdm import tqdm

from test_rule_based.rule_based_extractor import TimeEx


class DatasetLoader:

    def __init__(self, path_to_data_dir):
        self._path_to_data_dir = path_to_data_dir
        self._data_files = sorted(os.listdir(self._path_to_data_dir))

    def load_dataset(self):
        """
        загружает датасет из папки, путь к которой указывали в path_to_data_dir
        :return: список из (списоков кортежей (токен, тег) по одному на каждый файл)
        """
        texts = []
        for data_file in tqdm(self._data_files, desc='Loading data'):
            path_to_test_file = os.path.join(self._path_to_data_dir, data_file)
            if os.path.isdir(path_to_test_file):
                continue
            with open(path_to_test_file, 'r') as data_f:
                reader = csv.DictReader(data_f)
                sentence = []
                for row in reader:
                    sentence.append(row['token'])
                texts.append(sentence)
        return texts

    def add_to_dataset(self, data, column_name):
        """
        функция, которая записывает новую информацию в датасет
        :param data: список из списков кортежей (токен,  тег)
        :return:
        """
        for i, data_file in tqdm(enumerate(self._data_files), desc='Adding data'):
            path_to_test_file = os.path.join(self._path_to_data_dir, data_file)
            if os.path.isdir(path_to_test_file):
                continue
            with open(path_to_test_file, 'r') as data_f:
                reader = csv.DictReader(data_f)
                test_dir = os.path.join(self._path_to_data_dir, 'rules')
                if not os.path.exists(test_dir):
                    os.makedirs(test_dir)
                with open(os.path.join(test_dir, data_file), 'w', encoding='utf-8', newline='') as task:
                    fieldnames = ['token', 'tag', column_name]
                    writer = csv.DictWriter(task, fieldnames=fieldnames)
                    writer.writeheader()
                    for num, row in enumerate(reader):
                        new_row = row.copy()
                        token, pred_tag = data[i][num]
                        if row['token'] == token:
                            new_row[str(column_name)] = pred_tag
                        else:
                            new_row[str(column_name)] = ''
                        writer.writerow(new_row)

class Evaluator:
    """ Класс для оценки качества извлечения временных выражений """

    def __init__(self, file_dir, column_pred):
        self._predicted_files_dir = os.path.join(file_dir, 'rules')
        self._predicted_files = sorted(os.listdir(self._predicted_files_dir))
        self.column_pred = column_pred

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
                    preds_from_file.append(row[str(self.column_pred)])
                    targets_from_file.append(row['tag'])
                preds.append(preds_from_file)
                targets.append(targets_from_file)
        return preds, targets


if __name__ == '__main__':
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    path_to_data_dir = os.path.join(PROJECT_PATH, 'dataset', 'test')
    dataset_loader = DatasetLoader(path_to_data_dir)
    time_ex = TimeEx()
    # сохраняем набор тестовых данных
    samples = dataset_loader.load_dataset()
    print('Loaded {} sentences'.format(str(len(samples))))
    predictions = list()
    for text in samples:
        predictions.append(time_ex.rules(' '.join(text)))
    tag = 'predicted_rules_tag'
    dataset_loader.add_to_dataset(predictions, tag)
    evaluator = Evaluator(path_to_data_dir, tag)
    report = evaluator.evaluate()
    print(report)

