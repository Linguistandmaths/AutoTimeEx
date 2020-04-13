import re
from nltk.tokenize import WordPunctTokenizer
tk = WordPunctTokenizer()


class TimeEx:

    def __init__(self, text):
        self.text = text

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
        tokens = tk.tokenize(text)
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
            # когда I-тег находиться в середине, превращаем его в 'O'
            # (согласно шаблонам он не может оказаться начальным)
            token, tag = token_tuple
            if tag[0] == 'I':
                prev_tuple = result[index - 1]
                prev_token, prev_tag = prev_tuple
                if prev_tag[0] == 'O':
                    result[index] = (token, 'O')
            # преобразует начальный тег в серединный, если он оказывается внутри выражения
            if tag[0] == 'B':
                prev_tuple = result[index - 1]
                prev_token, prev_tag = prev_tuple
                if prev_tag[0] == 'B':
                    result[index] = (token, 'I'+tag[1:])
            # добавляем "-" в названия тегов
            if tag != 'O':
                result[index] = (token, tag[0]+'-'+tag[1:])
            # заменяем B-DATENUM на B-DATE
            if tag[-1] == 'M':
                result[index] = (token, 'B-DATE')
        return result

    def model(self, rulesResult):
        return rulesResult

    def merge(self, rulesResult, modelResult):
        return rulesResult


if __name__ == "__main__":
    text = input('enter your text: ')
    timex = TimeEx(text)
    print(timex.rules(text))
