def _extract_set(text, file_with_set):
    ''' загружаем примеры set из файла резултат храним списком в set_exaples'''
    with open((str(file_with_set), encoding='utf-8')) as f:
      set_examples = set(f.readlines())
    ''' перебираем токены из текста, список с кортежами храним в set '''
    set = []
    for token in text:
    # проверяем для примеров из одного слова
        if token in set_examples:
            set.append(token, 'B-SET')
            continue 
        else:
               #перебираем список из примеров из файла
            for set_ex in set_examples:
                if set_ex.startswith(token):
                    set.append(token, 'B-SET') 
                    break
                elif token in set_ex:
                    set.append(token, 'I-SET') 
                    break
                else:
                    set.append(token, 'O')
    return set
       
