import os
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict

from nltk.tokenize import WordPunctTokenizer
from ahocorapy.keywordtree import KeywordTree


class DataConverter:
    
    FIELDNAMES = ['token', 'type']

    def __init__(self):
        self._xml_files_dir = ''
        self._csv_files_dir = ''
        self._xml_files = sorted(os.listdir(self._xml_files_dir))
        self._csv_files = sorted(os.listdir(self._csv_files_dir))
        self._tokenizer = WordPunctTokenizer()

    def convert(self):
        """ Конвертация .xml файлов в .csv файлы, в которых перечислены токены и их типы в BIO-разметке """
        for xml_file in self._xml_files:
            if not xml_file.endswith('.tml'):
                continue
            xml_fname = xml_file[:-4]
            csv_fname = '{}.csv'.format(xml_fname)
            with open(os.path.join(self._csv_files_dir, csv_fname), 'w') as csv_f:
                writer = csv.DictWriter(csv_f, fieldnames=self.FIELDNAMES)
                tree = ET.parse(os.path.join(self._xml_files_dir, xml_file))
                root = tree.getroot()
                all_text, time_expressions = self._extract_text_and_time_expressions(root)
                all_tokens = self._tokenizer.tokenize(all_text)

                token_id2token_type = self._get_token_id2token_type(all_tokens, time_expressions)

                for i, token in enumerate(all_tokens):
                    if i in token_id2token_type:
                        writer.writerow({
                            'token': token,
                            'type': token_id2token_type[i]
                        })
                    else:
                        writer.writerow({
                            'token': token,
                            'type': 'O'
                        })

    def _get_token_id2token_type(self, all_tokens: List[str], time_expressions: Dict[str, List[str]]) -> Dict[int, str]:
        """
        Создаём словарь, в котором ключ - позиция токена в тексте, значение - его тип в BIO-разметке
        :param all_tokens: токенизированный текст
        :param time_expressions: словарь, который для каждого типа временного выражения содержит список токенов из
        текста
        :return: словарь, в котором ключ - позиция токена в тексте, значение - его тип в BIO-разметке
        """
        time_tree = self._create_kw_tree(time_expressions['TIME'])
        date_tree = self._create_kw_tree(time_expressions['DATE'])
        duration_tree = self._create_kw_tree(time_expressions['DURATION'])
        set_tree = self._create_kw_tree(time_expressions['SET'])
        token_id2token_type = dict()
        self._search_phrases(all_tokens, token_id2token_type, time_tree, 'TIME')
        self._search_phrases(all_tokens, token_id2token_type, date_tree, 'DATE')
        self._search_phrases(all_tokens, token_id2token_type, duration_tree, 'DURATION')
        self._search_phrases(all_tokens, token_id2token_type, set_tree, 'SET')
        return token_id2token_type

    def _extract_text_and_time_expressions(self, root):
        """
        Из xml файла достаём текст и временные выражения
        :param root: корень xml файла
        :return: all_text: текст (строка); time_expressions: словарь, где ключ - тип временного выражения, значение -
        список фраз из текста, имеющих соответствующий тип врменного выражения
        """
        all_text = ''
        time_expressions = {
            'TIME': [],
            'DATE': [],
            'DURATION': [],
            'SET': []
        }
        for text in root.iter('TEXT'):
            for t in text.itertext():
                all_text += t

            for time_expression in text.iter('TIMEX3'):
                text = time_expression.text
                type = time_expression.get('type')
                time_expressions[type].append(text)
        all_text = all_text.replace('\n', ' ')
        all_text = all_text.replace('  ', ' ')
        all_text = all_text.strip()
        return all_text, time_expressions

    def _create_kw_tree(self, time_expressions: List[str]) -> KeywordTree:
        """
        Создаёт суффиксное дерево для конкретного типа временного выражения
        :param time_expressions:
        :return: суффиксное дерево
        """
        kwtree = KeywordTree()
        for time_expression in time_expressions:
            tokens = self._tokenizer.tokenize(time_expression)
            kwtree.add(tokens)
        kwtree.finalize()
        return kwtree

    def _search_phrases(self, all_tokens: List[str], ids_time_expressions: Dict[int, str], kw_tree: KeywordTree,
                        type: str):
        """
        Ищет временные выражения в тексте, сохраняет в словарь ids_time_expressions для позиции токена в тексте тип
        временного выражения этого токена
        :param all_tokens: токенизированный текст
        :param ids_time_expressions: словарь, где ключ - позиция токена в тексте, значение - тип этого токена в BIO
        разметке; заполняется в этом методе
        :param kw_tree: суффиксное дерево соответствующего типа временного выражения
        :param type: тип временного выражения
        :return:
        """
        for ids in kw_tree.search_all(all_tokens):
            tokens = ids[0]
            for i, token in enumerate(tokens):
                if i == 0:
                    ids_time_expressions[ids[1] + i] = 'B-{}'.format(type)
                else:
                    ids_time_expressions[ids[1] + i] = 'I-{}'.format(type)


if __name__ == '__main__':
    data_converter = DataConverter()
    data_converter.convert()
