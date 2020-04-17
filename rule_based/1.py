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
        with open('regs', encoding='utf-8') as file:
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

        for index, token_tuple in enumerate(result):
            token, tag = token_tuple
            if index == 0:
                if tag[0] == 'I':
                    result[index] = (token, 'B' + tag[1:])
                else:
                    continue
            # elif index == len(result):
            elif tag != 'O':
                # когда I-тег находиться не в середине, превращаем его в 'O'
                # (согласно шаблонам он не может оказаться начальным)
                if tag[0] == 'I':
                    prev_tuple = result[index - 1]
                    prev_token, prev_tag = prev_tuple
                    try:
                        next_tuple = result[index + 1]
                        next_token, next_tag = next_tuple
                        if (prev_tag == 'O') and (next_tag == 'O'):
                            result[index] = (token, 'O')
                    except IndexError:
                        pass
                # преобразует начальный тег в серединный, если он оказывается внутри выражения
                elif tag[0] == 'B':
                    prev_tuple = result[index - 1]
                    prev_token, prev_tag = prev_tuple
                    if prev_tag != 'O':
                        result[index] = (token, 'I'+tag[1:])
                # заменяем B-DATENUM на B-DATE
                elif tag[-1] == 'M':
                    result[index] = (token, tag[:4])
                # добавляем "-" в названия тегов
        for index, token_tuple in enumerate(result):
            token, tag = token_tuple
            if tag != 'O':
                result[index] = (token, tag[0] + '-' + tag[1:])
        return result

    def model(self, rulesResult):
        return rulesResult

    def merge(self, rulesResult, modelResult):
        return rulesResult


if __name__ == "__main__":
    text = input('enter your text: ')
    timex = TimeEx()
    print(timex.rules(text))
