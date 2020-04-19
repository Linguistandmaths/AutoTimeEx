import re
import json
from nltk.tokenize import WordPunctTokenizer


class TimeEx:

    def __init__(self):
        self.tk = WordPunctTokenizer()
        with open('reg_exp/regexs_all.txt', encoding='utf-8') as file:
            whole_pattern_list = file.read().split('\n')
        self.whole_pattern = '|'.join(whole_pattern_list)

        self._special_tags = ['PUNCT', 'MONTH', 'WEEKDAY', 'TWODIGIT', 'FOURDIGIT']

        with open('map.json', encoding='utf-8') as mapp:
        self._mappings = json.load(mapp)

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
        parsed_tokens = self._find_special_tokens(tokens)
        processed_tokens = self._process_sequences(parsed_tokens)
        return processed_tokens

    def _find_special_tokens(self, tokens):
        """
        Находим "особые" токены, которые входят во временные выражения (например, числа, знаки препинания и т.д.)
        :param tokens: список токенов
        :return: список токенов с тэгом (PUNCT, TWODIGIT, etc.)
        """
        parsed_tokens = list()

        for token in tokens:
            # находит все токены, которые могут быть во временном выражении.
            found_timex = re.search(self.whole_pattern, token)
            if found_timex and found_timex.lastgroup:
                parsed_tokens.append((token, found_timex.lastgroup))
            else:
                parsed_tokens.append((token, 'O'))

        return parsed_tokens

    def _process_sequences(self, parsed_tokens):
        """
        Обрабатываем последовательность токенов с учётом их тэгов
        :param parsed_tokens: список токенов с тэгом (PUNCT, TWODIGIT, etc.)
        :return: список токенов с временным тэгом (B-DATE, B-DURATION , etc.)
        """
        processed_tokens = list()
        sequence = []
        sequence_tokens = []
        # идём по списку токенов
        for i, parsed_token in enumerate(parsed_tokens):
            token, token_tag = parsed_token
            # если у токена нет тэга и мы не нашли до этого последовательность тэгов, то в конечный результат добавляем токен и тэг 'O'
            if token_tag == 'O' and len(sequence) == 0:
                processed_tokens.append((token, token_tag))
            # если у токена нет тэга и мы уже нашли последовательность тэгов (например, In 1995 he was... мы сейчас на токене he)
            elif (token_tag == 'O' and len(sequence) > 0):
                sequence = ' '.join(sequence)
                # если последовательность есть маппинге временных тэгов, то запоминаем этот временной тэг, иначе - 'O'
                if sequence in self._mappings:
                    time_tag = self._mappings[sequence]
                else:
                    time_tag = 'O'
                # идём по токенам, которые нашли и проставляем тэг, найденный на прошлом этапе
                for i, sequence_token in enumerate(sequence_tokens):
                    if i == 0:
                        processed_tokens.append((sequence_token, 'B-{}'.format(time_tag)))
                    else:
                        processed_tokens.append((sequence_token, 'I-{}'.format(time_tag)))
                sequence = []
                sequence_tokens = []
            # ситуация, аналогичная предыдушей, но мы стоим на последнем токене введённой фразы
            elif (i == len(parsed_tokens) - 1 and len(sequence) > 0):
                sequence.append(token_tag)
                sequence_tokens.append(token)
                sequence = ' '.join(sequence)
                if sequence in self._mappings:
                    time_tag = self._mappings[sequence]
                else:
                    time_tag = 'O'
                for i, sequence_token in enumerate(sequence_tokens):
                    if i == 0:
                        processed_tokens.append((sequence_token, 'B-{}'.format(time_tag)))
                    else:
                        processed_tokens.append((sequence_token, 'I-{}'.format(time_tag)))
                sequence = []
                sequence_tokens = []
            # если это не тэг 'O' и не последний токен во фразе, то добавляем токен и тэг в последовательность
            else:
                sequence.append(token_tag)
                sequence_tokens.append(token)

        return processed_tokens

    def model(self, rulesResult):
        return rulesResult

    def merge(self, rulesResult, modelResult):
        return rulesResult


if __name__ == "__main__":
    text = input('enter your text: ')
    timex = TimeEx()
    print(timex.rules(text))
