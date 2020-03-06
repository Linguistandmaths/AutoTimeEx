import re


class TimeEx(object):

    def __init__(self, text):
        self.text = text

    def extract(self):
        """основная функция, которая вызывает другие и выдает конечный результат"""
        rulesResult = self.rules()
        modelResult = self.model(rulesResult)
        merged = self.merge(rulesResult, modelResult)
        return merged

    def rules(self):
        """функция с правилами сделана для таких слуучаев, чтобы был понятен алгоритм в целом,
        то есть для случаев с временным выражением из одного слова и для трех слов (the first of January).
        Названия тэгов исключительно как пример"""
        tokens = self.text.split(' ')
        result = []
        date_pattern = r'(?P<date_number>\d{2}\.\d{2}\.\d{4})'   # 22.22.2222
        time_pattern = r'(?P<time>\d{2}:\d{2})'   # 12:12
        Bdate_pattern = r'(?P<Bdate>first|second|third|fourth)'
        sign_pattern = r'(?P<sign>of)'
        Idate_pattern = r'(?P<Idate>[jJ]anuary|[fF]abruary|[mM]arch)'
        whole_pattern_list = [date_pattern, time_pattern, Bdate_pattern, sign_pattern, Idate_pattern]
        whole_pattern = '|'.join(whole_pattern_list)
        tags = ['date_number', 'time', 'Bdate', 'sign', 'Idate']

        for token in tokens:
            # находит все слова, которые могут быть во временном выражении. Т.е. пометит first, окружение не важно
            found_timex = re.search(whole_pattern, token)
            if found_timex:
                for tag in tags:
                    if found_timex.group(tag):
                        tuple_for_token = (token, tag)
                        result.append(tuple_for_token)
            else:
                tuple_for_token = (token, 'O')
                result.append(tuple_for_token)

        for token_tuple in result:
            # проверяет окружение, убирает ложно-положительные результаты
            index = result.index(token_tuple)
            token, tag = token_tuple
            if tag == 'Bdate':
                next_tuple = result[index + 1]
                next_token, next_tag = next_tuple
                if next_tag != 'sign':
                    result[index] = (token, 'O')

        return result

    def model(self,rulesResult):
        return rulesResult

    def merge(self, rulesResult, modelResult):
        return rulesResult


if __name__ == "__main__":
    text = input('enter your text: ')
    timex = TimeEx(text)
    print(timex.extract())
