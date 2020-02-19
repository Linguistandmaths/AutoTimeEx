# -*- coding: utf-8 -*-

import re

triggers = ['today', 'yesterday', 'tomorrow', 'at the weekend', 'tonight']
months_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_short = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
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
        # проверяем артикль на причастность к временной фразе
        elif token=='the':
            if token[cur_pos-1] in day_week:
                dates.append((token, 'I-DATE'))
                continue
            # проверяем идёт ли дальше число
            elif token[cur_pos+1].isnumeric():
                # удостоверяемся, что дальше есть слово. обозначающее месяц
                if (token[cur_pos+2] in months) or (token[cur_pos+3] in months):
                    # смотрим если перед артиклем день недели
                    if token[cur_pos-1] in day_week:
                        dates.append((token, 'I-DATE'))
                        continue
                    else:
                        dates.append((token, 'B-DATE'))
                        continue
            else:
                dates.append((token, 'O'))
                continue
        # ищем токен с названием месяца
        elif token in months:
            # проверяем есть ли до него или после числа или день недели
            if token[cur_pos - 1].isdigit() or (token[cur_pos - 1] in day_week):
                dates.append((token, 'I-DATE'))
                continue
            else:
                dates.append((token, 'B-DATE'))
                continue
        # проверка числового токена
        elif (len(token) <= 2) and (token.isdigit()=='True'):
            dates.append((token, 'B-DATE'))
        # 1790s такие типы
        elif (len(token) <= 5) and ((token.isnumeric()=='True') or (token.endswith('s'))):
            dates.append((token, 'B-DATE'))
        # проверка числа на то, что это год
        elif  (len(token)<=4) and (token.isdigit()=='True'):
            dates.append((token, 'B-DATE'))




return dates


(token.isdigit()=='True') or ()

and (token[cur_pos+1].endswith('d') or token[cur_pos+1].endswith('th'))

dates.append((token, 'O'))
    dates.append((token, 'B-DATE'))
    dates.append((token, 'I-DATE'))