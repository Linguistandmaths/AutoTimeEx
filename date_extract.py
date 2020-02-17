# -*- coding: utf-8 -*-

import re

triggers = ['today', 'yesterday', 'tomorrow', 'at the weekend', 'tonight']
months_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
week_long = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
week_short = ['Mon', 'Tue', 'Wed', 'Sat', 'Sun']
numbers = ['first', 'second']
months = months_long + months_short
day_week = week_short + week_long


# get extracted information DATE with words
result = []
for t in tokens:
    if t in months:
        pos_month = tokens.index(t)
        result.append(t)
        start = pos_month - 2
        end = pos_month + 2
        for el in tokens[start:end]:
            if el in day_week:
                result.append('day of the week is '+el)
            elif el.endswith('th'):
                day = re.sub('th', '', el)
                result.append('day is ' + day)
            elif el.endswith('d'):
                day = re.sub('d', '', el)
                result.append('day is ' + day)
            try:
                if type(int(el)) == int:
                    if (len(el) == 1) or (len(el) == 2):
                        result.append('day is '+el)
                    elif len(el) == 4:
                        result.append('year is '+el)
            except:
                pass
print(result)


# функция ищет нечисловые паттерны из таблицы
def _extract_date(text):
    dates = []
    # перебираем токены из текста, список с кортежами храним в dates
    for token in text:
        cur_pos = text.index(token)
        # определяем день недели это или нет
        if token in day_week:
            dates.append((token, 'B-DATE'))
            continue
        # проверяем артиклб на причастность к временной фразе
        elif token=='the':
            if token[cur_pos-1] in day_week:
                dates.append((token, 'I-DATE'))
                continue
            # проверяем идёт ли дальше порядковое
            elif (int(token[cur_pos+1][:-2]) ) and ((token[cur_pos+1].endswith('d')) or (token[cur_pos+1].endswith('th'))):
                dates.append((token, 'I-DATE'))
            else:
                dates.append((token, 'O'))
                continue
        # ищем токен с названием месяца
        elif token in months:
            # проверяем есть ли до него или после числа
            if token[cur_pos - 1]
                dates.append((token, 'I-DATE'))
                continue
            elif token[cur_pos + 1]
                dates.append((token, 'B-DATE'))
                continue
        # проверка числового токена
        if len(token) <= 2:


        # проверка числа на то, что это год
        if len(token) <= 4:




    return dates


dates.append((token, 'O'))
    dates.append((token, 'B-DATE'))
    dates.append((token, 'I-DATE'))