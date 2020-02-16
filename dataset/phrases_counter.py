import os
import xml.etree.ElementTree as ET


class PhrasesCounter:

    def __init__(self):
        self._dataset_path = ''

    def get_phrases_for_types(self):
        """ Записывает в файл временные выражения (уникальные) для каждого типа """
        type2phrases = self._parse_xml_files()
        with open('phrases_by_types.txt', 'w') as f:
            for type, phrases in type2phrases.items():
                f.write('{}: {} unique phrases\n'.format(type, str(len(phrases))))
                phrases = sorted(list(phrases))
                for phrase in phrases:
                    f.write(phrase + '\n')
                f.write('\n')

    def _parse_xml_files(self):
        """
        Парсит xml файлы и извлекается временные выражения для каждого типа
        :return: словарь, где ключ - тип временного выражения, значение - множество уникальных временных выражений,
        найденных в корпусе
        """
        type2phrases = dict()
        for f in os.walk(self._dataset_path):
            files = f[2]
            dir_path = f[0]
            for fname in files:
                if not fname.endswith('.tml'):
                    continue
                tree = ET.parse(os.path.join(dir_path, fname))
                root = tree.getroot()
                for text in root.iter('TEXT'):
                    for time_expression in text.iter('TIMEX3'):
                        text = time_expression.text
                        type = time_expression.get('type')
                        if type in type2phrases:
                            type2phrases[type].add(text)
                        else:
                            type2phrases[type] = {text}
        return type2phrases


if __name__ == '__main__':
    phrases_counter = PhrasesCounter()
    phrases_counter.get_phrases_for_types()
