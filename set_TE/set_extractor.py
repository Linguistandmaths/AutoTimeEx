import os
import csv

from tqdm import tqdm


def _extract_set(text, file_with_set):
    """загружаем примеры set из файла резултат храним списком в set_exaples
    """
    with open(str(file_with_set), encoding='utf-8') as f:
        set_examples = set(f.readlines())
    ''' перебираем токены из текста, список с кортежами храним в set '''
    res_set = []
    for token in text:
        # проверяем для примеров из одного слова
        if token in set_examples:
            res_set.append((token, 'B-SET'))
            continue 
        else:
            # перебираем список из примеров из файла
            for set_ex in set_examples:
                if set_ex.startswith(token):
                    res_set.append((token, 'B-SET'))
                    break
                elif token in set_ex:
                    res_set.append((token, 'I-SET'))
                    break
                else:
                    res_set.append((token, 'O'))
    return res_set


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
    with open('set_result.csv', 'w', encoding='utf-8') as result:
        writer = csv.writer(result)
        for sentence in sentences:
            res = _extract_set(sentence,'list_set_type.txt')
            writer.writerows(res)


