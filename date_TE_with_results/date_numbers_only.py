import re


def date_extraction(text):

    threeGroupsDate = r'\d{2,4}[\/\-.]\d{2}[.\-\/]\d{2,4}'   # 14.12.1999, 1999.12.14, 12.14.1999
    yearFirst = r'[1-9]\d{3}[\.-\/][0-1]\d[\.-\/][0-3]\d'   # 1999.14.12
    yearLast = r'[0-3]\d{1}[\.-\/][0,1]\d[\.-\/][1-9]\d{3}'   # 14.12.1999
    yearLastShort = r'[0-3]\d{1}[\.-\/][0,1]\d[\.-\/][1-9]\d'   # 14.12.99
    monthAndYear = r'[0,1]\d[\.-\/][1-2]\d{3}'   # 12.1999
    dateAndMonth = r'[0-3]\d[\.\/-][0,1]\d'   # 14.12, 03.01
    finalRuleList = [threeGroupsDate, yearFirst, yearLast, yearLastShort, monthAndYear, dateAndMonth]
    finalRule = '|'.join(finalRuleList)
    result = re.findall(finalRule, text)
    return result


if __name__ == '__main__':
    file = open('XIE19990313.0229.tml', 'r')
    text = file.read()

    listWithTimexes = date_extraction(text)
    print(listWithTimexes)
