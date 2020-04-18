import re
from nltk.tokenize import WordPunctTokenizer


class TimeEx:

    def __init__(self):
        self.tk = WordPunctTokenizer()

    def extract(self, text):
        """основная функция, которая вызывает другие и выдает конечный результат"""
        rulesResult = self.rules(text)
        modelResult = self.model(rulesResult)
        merged = self.merge(rulesResult, modelResult)
        return merged

    def rules(self, text):
        """
        функция, применяющая регулярные выражения
        :param text: строка
        :return: кортеж (токен, тег)
        """
        # токенизация входной строки
        tokens = self.tk.tokenize(text)
        result = []
        # загружаю регулярки из общего файла, где нет повторяющихся классов
        with open('reg_exp/regexs_all_together.txt', encoding='utf-8') as file:
            whole_pattern_list = file.read().split('\n')
        whole_pattern = '|'.join(whole_pattern_list)
        tags = ['BDATE', 'IDATE', 'BDATENUM', 'BTIME', 'ITIME', 'BDURATION', 'IDURATION', 'BSET', 'ISET']

        for token in tokens:
            # находит все слова, которые могут быть во временном выражении.
            found_timex = re.search(whole_pattern, token)
            if found_timex:
                for tag in tags:
                    try:
                        if found_timex.group(tag):
                            tuple_for_token = (token, tag)
                            result.append(tuple_for_token)
                    except IndexError:
                        continue
            else:
                print(token)
                tuple_for_token = (token, 'O')
                result.append(tuple_for_token)

        # добавляем "B-, I-" в названия тегов
        for index, token_tuple in enumerate(result):
            token, tag = token_tuple
            if tag != 'O':
                if index == 0:
                    result[index] = (token, 'B-' + tag)
                else:
                    prev_token, prev_tag = result[index-1]
                    if prev_tag == 'O':
                        result[index] = (token, 'B-' + tag)
                    else:
                        result[index] = (token, 'I-' + tag)

        return result

    def model(self, rulesResult):
        return rulesResult

    def merge(self, rulesResult, modelResult):
        return rulesResult


if __name__ == "__main__":
    text = input('enter your text: ')
    timex = TimeEx()
    print(timex.rules(text))
