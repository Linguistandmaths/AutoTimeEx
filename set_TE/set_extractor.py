import os
import csv

from tqdm import tqdm
from ahocorapy.keywordtree import KeywordTree


class SetTE:
    def __init__(self):
        pass

    def _extract_set(self, tokens):
        """загружаем примеры set из файла резултат храним списком в set_exaples
        :param tokens - список токенов
        :return res_set - список примеров взодящих в строку
        """
        file_with_set = r'list_set_type.txt'
        with open(file_with_set, encoding='utf-8') as f:
            set_examples = f.read().split('\n')
        set_examples = set(set_examples)
        print(set_examples)
        ''' перебираем токены из текста, список с кортежами храним в set '''
        res_set = []
        text = ' '.join(tokens)
        for set_ex in set_examples:
            if set_ex in text:
                res_set.append(set_ex)
        return res_set


    def _create_kw_tree(self, tokens_set):
        """
        Создаёт суффиксное дерево для конкретного типа временного выражения
        :param time_expressions:
        :return: суффиксное дерево
        """
        kwtree = KeywordTree()
        for date in tokens_set:
            tokens = date.split()
            kwtree.add(tokens)
        kwtree.finalize()
        return kwtree


    def _search_phrases(self, all_tokens, ids_time_expressions, kw_tree: KeywordTree, type):
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


    def _get_token_id2token_type(self, all_tokens):
        """
        Создаём словарь, в котором ключ - позиция токена в тексте, значение - его тип в BIO-разметке
        :param all_tokens: токенизированный текст
        :param time_expressions: словарь, который для каждого типа временного выражения содержит список токенов из
        текста
        :return: словарь, в котором ключ - позиция токена в тексте, значение - его тип в BIO-разметке
        """
        tokens_date = self._extract_set(all_tokens)
        time_tree = self._create_kw_tree(tokens_date)
        token_id2token_type = dict()
        self._search_phrases(all_tokens, token_id2token_type, time_tree, 'SET')
        return token_id2token_type


    def extract(self, text):
        if type(text) == list:
            all_tokens = text
        else:
            all_tokens = text.split()
        token_id2token_type = self._get_token_id2token_type(all_tokens)

        result_tuples = []
        for i, token in enumerate(all_tokens):
            if i in token_id2token_type:
                result_tuples.append((token, token_id2token_type[i]))
            else:
                result_tuples.append((token, 'O'))
        return result_tuples


# считываем файлы с тестовой выборкой, токены соединяются по точке
def load_dataset(path_to_data_dir):
    data_files = sorted(os.listdir(path_to_data_dir))
    test_sentences = []
    for data_file in tqdm(data_files, desc='Loading data'):
        with open(os.path.join(path_to_data_dir, data_file), 'r') as data_f:
            reader = csv.DictReader(data_f)
            sentence = []
            for row in reader:
                if row['token'] == '.':
                    sentence.append(row['token'])
                    test_sentences.append(sentence)
                    sentence = []
                    continue
                else:
                    sentence.append(row['token'])
    return test_sentences


# process test dataset by rules
if __name__ == '__main__':
    path_to_data_dir = r'/Users/anast/PycharmProjects/AutoTimeEx/test'
    sentences = load_dataset(path_to_data_dir)
    print('Loaded {} sentences'.format(str(len(sentences))))
    set_te = SetTE()
    with open('set_result.csv', 'w', encoding='utf-8') as result:
        writer = csv.writer(result)
        for sentence in sentences:
            res = set_te.extract(sentence)
            writer.writerows(res)


