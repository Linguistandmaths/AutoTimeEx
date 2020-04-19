import os
import csv

from seqeval.metrics import classification_report


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
    evaluator = Evaluator()
    report = evaluator.evaluate()
    print(report)
