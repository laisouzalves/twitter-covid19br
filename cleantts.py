import re

accent_map = {u'\u00c0': u'A', u'\u00c1': u'A', u'\u00c2': u'A', u'\u00c3': u'A', u'\u00c4': u'A', u'\u00c5': u'A', u'\u00c6': u'A', u'\u00c7': u'C', u'\u00c8': u'E', u'\u00c9': u'E', u'\u00ca': u'E', u'\u00cb': u'E', u'\u00cc': u'I', u'\u00cd': u'I', u'\u00ce': u'I', u'\u00cf': u'I', u'\u00d0': u'D', u'\u00d1': u'N', u'\u00d2': u'O', u'\u00d3': u'O', u'\u00d4': u'O', u'\u00d5': u'O', u'\u00d6': u'O', u'\u00d7': u'x', u'\u00d8': u'0', u'\u00d9': u'U', u'\u00da': u'U', u'\u00db': u'U', u'\u00dc': u'U', U'\u00dd': u'Y', u'\u00df': u'B', u'\u00e0': u'a', u'\u00e1': u'a', u'\u00e2': u'a', u'\u00e3': u'a', u'\u00e4': u'a', u'\u00e5': u'a', u'\u00e6': u'a', u'\u00e7': u'c', u'\u00e8': u'e', u'\u00e9': u'e', u'\u00ea': u'e', u'\u00eb': u'e', u'\u00ec': u'i', u'\u00ed': u'i', u'\u00ee': u'i', u'\u00ef': u'i', u'\u00f1': u'n', u'\u00f2': u'o', u'\u00f3': u'o', u'\u00f4': u'o', u'\u00f5': u'o', u'\u00f6': u'o', u'\u00f8': u'0', u'\u00f9': u'u', u'\u00fa': u'u', u'\u00fb': u'u', u'\u00fc': u'u'}


def accent_remove(m):
    return accent_map[m.group(0)]

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
    
def clean_tts(list_to_clean):
    for idx, item in enumerate(list_to_clean):
        # transforma tudo para str
        list_to_clean[idx] = str(item)
        # retira todo o link https:// do tuite
        list_str = list_to_clean[idx].split()
        string = ' '.join([word for word in list_str if not re.search('https://t.co', word)])
        #remove acentos
        list_to_clean[idx] = re.sub(u'([\u00C0-\u00FC])', accent_remove, string.encode().decode('utf-8'))
        # remove emojis
        string = list_to_clean[idx].encode('ascii', 'ignore').decode('ascii')
        list_to_clean[idx] = remove_emoji(string)
        # deixa tudo em caixa baixa
        list_to_clean[idx] = list_to_clean[idx].lower()
        # substitui o restante dos caracteres desnecessarios
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('[…•\-\(\)\&]', '', string)
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('\W\s-', '', string)
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('["º°/_]', ' ', string)
        # separa pontuações no final das palavras
        char = '...'
        string = list_to_clean[idx]
        res = [i for j in string.split(char) for i in (j, char)][:-1] 
        list_to_clean[idx] = ' '.join(res)
        char = '?'
        string = list_to_clean[idx]
        res = [i for j in string.split(char) for i in (j, char)][:-1] 
        list_to_clean[idx] = ' '.join(res) 
        char = '!'
        string = list_to_clean[idx]
        res = [i for j in string.split(char) for i in (j, char)][:-1] 
        list_to_clean[idx] = ' '.join(res)
        char = '.'
        string = list_to_clean[idx]
        res = [i for j in string.split(char) for i in (j, char)][:-1] 
        list_to_clean[idx] = ' '.join(res)
        char = ','
        string = list_to_clean[idx]
        res = [i for j in string.split(char) for i in (j, char)][:-1] 
        list_to_clean[idx] = ' '.join(res)
        # remove palavras de comprimento menor que 3
        string_list = list_to_clean[idx].split() 
        strings = [x for x in string_list if len(x)>2]
        list_to_clean[idx] = ' '.join(strings)
        # remove espaços desnecessarios
        string_list = list_to_clean[idx].split()
        list_to_clean[idx] = ' '.join(string_list)
    return list_to_clean
