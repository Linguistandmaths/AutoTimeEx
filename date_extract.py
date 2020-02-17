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

# on Tuesday
for t in token:
    if (t == 'on') and (token[token.index(t)+1] in day_week):
        result.append(token[token.index(t)+1])



def _extract_date(text):
    date = []
    # перебираем токены из текста, список с кортежами храним в date
    for token in text:
        if token in months:




    return date
