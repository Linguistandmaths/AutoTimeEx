import re
import json
from nltk.tokenize import WordPunctTokenizer


class TimeEx:
    """ Класс для определения типа временного выражения"""

    def __init__(self):
        self.tk = WordPunctTokenizer()
        with open('reg_exp/regexs_all.txt', encoding='utf-8') as file:
            whole_pattern_list = file.read().split('\n')
        self.whole_pattern = '|'.join(whole_pattern_list)

        # названия групп
        self._special_tags = []
        for tag in re.findall(r'\?P<\w{1,}>', self.whole_pattern):
            self._special_tags.append(tag.strip('<>?P'))

        # загружаем из файла соотношение последовательностей с типами временных выражений
        with open('map.json', encoding='utf-8') as mapp:
            self._mappings = json.load(mapp)

    def extract(self, text):
        """
        основная функция, которая вызывает другие и выдает конечный результат
        :param text: строка
        :return: кортеж (токен, тег)
        """
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
            # если у токена нет тэга и мы уже нашли последовательность тэгов
            # (например, In 1995 he was... мы сейчас на токене he)
            if token_tag == 'O':
                if len(sequence) > 0:
                    sequence = ' '.join(sequence)
                    # если последовательность есть маппинге временных тэгов, то запоминаем этот временной тэг
                    if sequence in self._mappings:
                        time_tag = self._mappings[sequence]
                        # идём по токенам, которые нашли и проставляем тэг, найденный на прошлом этапе
                        for num, sequence_token in enumerate(sequence_tokens):
                            if num == 0:
                                processed_tokens.append((sequence_token, 'B-{}'.format(time_tag)))
                            else:
                                processed_tokens.append((sequence_token, 'I-{}'.format(time_tag)))
                    # если последовательности нет в маппинге, то проставляем "O"
                    else:
                        time_tag = 'O'
                        for sequence_token in sequence_tokens:
                            processed_tokens.append((sequence_token, time_tag))
                        processed_tokens.append((token, token_tag))
                    sequence = []
                    sequence_tokens = []
                # если у токена нет тэга и мы не нашли до этого последовательность тэгов,
                # то в конечный результат добавляем токен и тэг 'O'
                else:
                    processed_tokens.append((token, token_tag))
            else:
                # у токена есть тег и это последний токен в фразе
                if i == (len(parsed_tokens) - 1):
                    sequence.append(token_tag)
                    sequence_tokens.append(token)
                    sequence = ' '.join(sequence)
                    if sequence in self._mappings:
                        time_tag = self._mappings[sequence]
                        # идём по токенам, которые нашли и проставляем тэг, найденный на прошлом этапе
                        for num, sequence_token in enumerate(sequence_tokens):
                            if num == 0:
                                processed_tokens.append((sequence_token, 'B-{}'.format(time_tag)))
                            else:
                                processed_tokens.append((sequence_token, 'I-{}'.format(time_tag)))
                    # если последовательности нет в маппинге, то проставляем "O"
                    else:
                        time_tag = 'O'
                        for sequence_token in sequence_tokens:
                            processed_tokens.append((sequence_token, time_tag))
                    sequence = []
                    sequence_tokens = []
                # у токена есть тег и это не последний токен во фразе
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
