import pandas as pd
import re
from baseuf import ufbr
from collections import Counter
import csv
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

################### FUNCTIONS USED IN THIS SCRIPT ###################

accent_map = {u'\u00c0': u'A', u'\u00c1': u'A', u'\u00c2': u'A', u'\u00c3': u'A', u'\u00c4': u'A', u'\u00c5': u'A', u'\u00c6': u'A', u'\u00c7': u'C', u'\u00c8': u'E', u'\u00c9': u'E', u'\u00ca': u'E', u'\u00cb': u'E', u'\u00cc': u'I', u'\u00cd': u'I', u'\u00ce': u'I', u'\u00cf': u'I', u'\u00d0': u'D', u'\u00d1': u'N', u'\u00d2': u'O', u'\u00d3': u'O', u'\u00d4': u'O', u'\u00d5': u'O', u'\u00d6': u'O', u'\u00d7': u'x', u'\u00d8': u'0', u'\u00d9': u'U', u'\u00da': u'U', u'\u00db': u'U', u'\u00dc': u'U', U'\u00dd': u'Y', u'\u00df': u'B', u'\u00e0': u'a', u'\u00e1': u'a', u'\u00e2': u'a', u'\u00e3': u'a', u'\u00e4': u'a', u'\u00e5': u'a', u'\u00e6': u'a', u'\u00e7': u'c', u'\u00e8': u'e', u'\u00e9': u'e', u'\u00ea': u'e', u'\u00eb': u'e', u'\u00ec': u'i', u'\u00ed': u'i', u'\u00ee': u'i', u'\u00ef': u'i', u'\u00f1': u'n', u'\u00f2': u'o', u'\u00f3': u'o', u'\u00f4': u'o', u'\u00f5': u'o', u'\u00f6': u'o', u'\u00f8': u'0', u'\u00f9': u'u', u'\u00fa': u'u', u'\u00fb': u'u', u'\u00fc': u'u'}


def accent_remove(m):
    return accent_map[m.group(0)]


def clean_list(list_to_clean):
    for idx, item in enumerate(list_to_clean):
        list_to_clean[idx] = str(item)
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('[÷ð]', '', string)
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub(u'([\u00C0-\u00FC])', accent_remove, string.encode().decode('utf-8'))
        list_to_clean[idx] = list_to_clean[idx].lower()
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('\W\s-', '', string)
        string = list_to_clean[idx]
        list_to_clean[idx] = re.sub('[…•\(\)\&]', ' ', string)
    return list_to_clean

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
        # remove espaços desnecessarios
        string_list = list_to_clean[idx].split()
        list_to_clean[idx] = ' '.join(string_list)

    return list_to_clean

def filter_count(principal_list, filter1):
    count_filter = 0
    bool_list = []
    for idx, item in enumerate(principal_list):
        frase = item
        if ' - ' in frase:
            frase = frase.split(' - ')
        elif ' -' in frase:
            frase = frase.split(' -')
        elif '- ' in frase:
            frase = frase.split('- ')
        elif '-' in frase:
            frase = frase.split('-')
        elif ' / ' in frase:
            frase = frase.split(' / ')
        elif ' /' in frase:
            frase = frase.split(' /')
        elif '/ ' in frase:
            frase = frase.split('/ ')
        elif '/' in frase:
            frase = frase.split('/')
        elif ' , ' in frase:
            frase = frase.split(' , ')
        elif ', ' in frase:
            frase = frase.split(', ')
        elif ' ,' in frase:
            frase = frase.split(' ,')
        elif ',' in frase:
            frase = frase.split(',')
        elif ' | ' in frase:
            frase = frase.split(' | ')
        elif ' |' in frase:
            frase = frase.split(' |')
        elif '| ' in frase:
            frase = frase.split('| ')
        elif '|' in frase:
            frase = frase.split('|')

        if type(frase) != list:
            frase = [frase]

        for idx, item in enumerate(filter1):
            if item in frase:
                count_filter += 1
                bool_list.append(True)
                break
            if item == filter1[-1]:
                bool_list.append(False)

    return count_filter, bool_list

# def cities_tolist(city_list):
#     cities = []
#     for idx, item in enumerate(city_list):
#         city = item.lower()
#         cities.append(city)
#     return cities

estados = [['acre', 'ac'], ['alagoas', 'al'], ['amazonas', 'am'], ['amapa', 'ap'], ['bahia', 'bahea', 'ba'],  ['ceara', 'ce'], ['distrito federal', 'de-efe', 'brasolia', 'df', 'taguatinga', 'asa sul', 'sobradinho', 'ceilandia', 'samambaia', 'asa norte', 'guara', 'aguas claras', 'parkway', 'vicente pires'], ['espirito santo', 'es'], ['goias', 'gyn', 'go'], ['maranhao', 'terehell', 'ma'], ['minas gerais', 'mg'], ['mato grosso do sul', 'ms'], ['mato grosso', 'mt'], ['para', 'pa'], ['paraiba', 'pb'], ['pernambuco', 'pe'], ['piaui', 'pi'], ['parana', 'pr'], ['rio de janeiro', 'rj'], ['rio grande do norte', 'rn'], ['rondonia', 'ro'], ['roraima', 'rr'], ['rio grande do sul', 'rs'], ['santa catarina', 'sc'], ['sergipe', 'se'], ['sao paulo', 'sampa', 'sp'], ['tocantins', 'to']]

def separar_estados(lista_locais, csvFile_):
    c_lista_locais = clean_list(lista_locais)
    dataframe = pd.DataFrame(columns=['state', 'tts_count'])
    # ufbr.list_uf = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    for idx, item in enumerate(ufbr.list_uf):
        # Example: cidades_sp = ufbr.list_cidades('SP')
        # cities_tolist() limpa a lista de cidades (set lower, splits, exclude "de" and "da")
        cities = cities_tolist(ufbr.list_cidades(item)) + estados[idx]
        # c_cities contains the list of cities without any pontuation
        c_cities = clean_list(cities)
        # cities_count(states_list) é o numero de tweets na lista states_list
        cities_count, has_place_list = filter_count(c_lista_locais, c_cities)
        row_to_append = [str(item), cities_count]
        row = pd.DataFrame([row_to_append], columns=['state', 'tts_count'])
        dataframe = dataframe.append(row, ignore_index=True)

    dataframe.to_csv(csvFile_, mode='a', columns=['state', 'tts_count'], header=True, index=False, encoding="utf-8")

########################### USER INPUT ###########################
print("This script takes a file containing the tweets from tweepy.Cursor and returns a cleaned version of the file and prints some important insights from the data.")
print('----------------------------------------------------------------')
csvFile = str(input(">>> Enter file name: "))
print("\n>>> Reading {}...".format(csvFile))
data = pd.read_csv(csvFile)
data.rename(columns = {'created_at' : 'date', 'original_text' : 'text', 'place_coord_boundaries' : 'geo'}, inplace=True)


# drop_column0 = insert("The file contains 'Unnamed: 0' has a first column? (insert True or False): ")
# if drop_column0 != True and drop_column0 != False:
#     drop_column0 = False
# if drop_column0 == True:
#     data.drop(columns=['Unnamed: 0'], inplace=True)

print('---------------------------------------------------------')
print('_________________________________________________________\n')

print("                    TWEETS REPORT                        ")
print('_________________________________________________________')
print('---------------------------------------------------------')

######################## NUMBER OF TWEETS ########################

num_tweets = data.shape[0]
print("Número total de tweets: {}".format(num_tweets))
print('---------------------------------------------------------')

df_full = data[['id', 'date', 'text', 'geo', 'hashtags', 'place']]

######################## GEOGRAPHIC ANALYSIS ########################

estados_list = ['acre', 'ac', 'alagoas', 'al', 'amapa', 'ap', 'amazonas', 'am', 'bahia', 'ba', 'ceara', 'ce', 'distrito federal', 'df', 'espirito santo', 'es', 'goias', 'go', 'maranhao', 'ma', 'mato grosso', 'mt', 'mato grosso do sul', 'ms', 'minas gerais', 'mg', 'para', 'pa', 'paraiba', 'pb', 'parana', 'pr', 'pernambuco', 'pe', 'piaui', 'pi', 'rio de janeiro', 'rj', 'rio grande do norte', 'rn', 'sul', 'rs', 'rondonia', 'ro', 'roraima', 'rr', 'santa catarina', 'sc', 'sao paulo', 'sp', 'sergipe', 'se', 'tocantins', 'to']

capitais = ['rio branco', 'maceio', 'macapa', 'manaus', 'salvador', 'fortaleza', 'brasilia', 'bsb', 'vitoria', 'goiania', 'gyn', 'sao luis', 'cuiaba', 'campo grande', 'belo horizonte', 'bh', 'belem', 'joao pessoa', 'jp', 'curitiba', 'recife', 'teresina', 'terehell', 'rio de janeiro', 'rj', 'natal', 'porto alegre', 'poa', 'porto velho', 'boa vista', 'florianopolis', 'floripa', 'sao paulo', 'sampa', 'aracaju', 'palmas']

# all_cities = []
# for idx, item in enumerate(ufbr.list_uf):
#     city_list = cities_tolist(ufbr.list_cidades(item))
#     for idx, item in enumerate(city_list):
#         all_cities.append(item)
#
# troquei pelo de baixo:

all_cities = []
for item in ufbr.list_uf:
    city_list = [x.lower() for x in ufbr.list_cidades(item)]
    all_cities += city_list

locais_br = all_cities + estados_list + ['brasil', 'brazil']
c_locais_br = clean_list(locais_br)

places = df_full['place'].to_list()
c_places = clean_list(places)

# places_idx = []
# for idx, item in enumerate(c_places):
#     string = str(item)
#     for i, j in enumerate(string.split()):
#         if j in c_locais_br and idx not in places_idx:
#             places_idx.append(idx)
#
# troquei pelo o de baixo pq arrumei a função filter_count()

print("Colecting 'has_place' column...")
num_places_br, has_place = filter_count(c_places, c_locais_br)
print("Done colecting 'has_place' column.")

mask = df_full['place'].notnull()
data_all_places = df_full[mask]

print("Número total de tweets com local preenchido {}.\nIsso equivale a {:.2f} % dos tweets.\n".format(data_all_places.shape[0], data_all_places.shape[0]*100/data.shape[0]))

# print("Número total de twittes que possuem local válido: {}.\nIsso equivale à {:.2f}% do total de twittes.".format(len(places_idx), len(places_idx)*100/len(c_places)))
print("Número total de twittes que possuem local válido: {}.\nIsso equivale à {:.2f}% do total de twittes.".format(num_places_br, num_places_br*100/data.shape[0]))
print('---------------------------------------------------------')

# has_place = list(range(0, len(df_full['place'])))
# for idx,item in enumerate(df_full['place']):
#     if idx in places_idx:
#         has_place[idx] = True
#     else:
#         has_place[idx] = False

has_place = pd.DataFrame(has_place, columns=['has_place'])
new_data = pd.concat([df_full, has_place], axis=1)
print(">>> New column 'has_place' has been concatenated")
try:
    if new_data['Unnamed: 0'].any():
        print("Droping column 'Unnamed: 0'")
        new_data.drop(columns=['Unnamed: 0'], inplace=True)
except KeyError:
    print('---------------------------------------------------------')

## DataFrame with all the valid places:
mask = new_data['has_place'] == True
data_valid_places = new_data[mask]

## List with all valid places:
places_list = data_valid_places['place'].to_list()

csvFile_places = str(input(">>> Enter name for the output csv file for the number of tweets per state (ex.: tweets-per-state.csv): "))
separar_estados(places_list, csvFile_places)

count = pd.read_csv(csvFile_places) # tts-por-estado.csv
number_of_tts = count['tts_count'].sum()

print("Total de tweets com 'place' do Brasil: {}".format(number_of_tts))
print('---------------------------------------------------------')

########################## RT ANALYSIS ################################

tweets = new_data['text'].tolist()
tweets = [str(x) for x in tweets]

tweets_RT = sum(1 for x in tweets if x.count('RT @'))

print("Total de RTs : {}".format(tweets_RT))
print("Isso equivale a {:.2f}% do número total de tweets.".format(tweets_RT*100/len(tweets)))
print('---------------------------------------------------------')


is_rt = []
rt_pattern = 'RT @'
original_tts = new_data['text'].tolist()
for idx, item in enumerate(original_tts):
    string = str(item)
    if string.find(rt_pattern) == 0:
        is_rt.append(True)
    else:
        is_rt.append(False)

is_rt = pd.DataFrame(is_rt, columns=['is_rt'])
new_data_rt = pd.concat([new_data, is_rt], axis=1)
print(">>> New column 'is_rt' has been concatenated")
try:
    if new_data_rt['Unnamed: 0'].any():
        print("Droping column 'Unnamed: 0'")
        new_data_rt.drop(columns=['Unnamed: 0'], inplace=True)
except KeyError:
    print('---------------------------------------------------------')

fileName = str(csvFile[:-4]+'_new.csv')
new_data_rt.to_csv(fileName)
print(">>> New file '{}' has been created.".format(fileName))

################ SELECTING DATA TO WORD CLOUD ######################

mask = new_data_rt['is_rt'] == False
cloud_data = new_data_rt[mask]
mask = cloud_data['has_place'] == True
cloud_data = cloud_data[mask]

clean_tuites = cloud_data['text'].to_list()
clean_tuites = clean_tts(clean_tuites)

word_list = []
stop_words = ['e', 'de', 'a', 'as', 'da', 'das', 'o', 'os', 'aos', 'do', 'dos', 'que', 'em', 'com', 'para', 'n', 'no', 'na', 'um', 'se', 'pra', 'este', 'esta', 'pro', 'me', 'ao', 'ou', 'esse', 'essa', 'q', 'p', 'nas', 'pq', 'tao', 'entao', 'te', 'porque', '1', '2', '3', '4', '5', '7', '10', '...', '.', ',', '?', '!', '|', ':', '#', '@']
print(">>> Saving file 'nuvem_palavras.txt'...")
with open('nuvem_palavras.txt', 'w') as wf:
    for phrase in clean_tuites:
        for word in phrase.split():
            if word not in stop_words:
                if word[-1] == '.' or word[-1] == ',':
                    word_list.append(str(word[:-1]))
                else:
                    word_list.append(str(word))
                wf.write(word + ' ')

words_count = Counter(word_list)
df_words_count = pd.DataFrame(words_count.items(), columns=['word', 'count'])
df_words_count = df_words_count.sort_values(by=['count'], ascending=False).reset_index(drop=True)
print(">>> Saving file 'words_count.csv'...")
df_words_count.to_csv('words_count.csv')
# with open('words_count.csv','wb') as f:
#     w = csv.writer(f)
#     w.writerows(words_count.items())

############ PLOTING NUMBER OF TWEETS PER DAY ###################

dates = new_data_rt['date'].to_list()

clean_datas = []
for idx, item in enumerate(dates):
    string = str(item)
    day = string[8:10]
    month = string[4:7]
    if month == 'Apr':
        month = '04'
        clean_datas.append('{}-{}'.format(month, day))
    else:
        month = '03'
        clean_datas.append('{}-{}'.format(month, day))

counts = Counter(clean_datas)
df_num_tts = pd.DataFrame(counts.items(), columns=['date', 'num_tts'])
df_num_tts = df_num_tts.sort_values(by=['date']).reset_index(drop=True)

sns_plot = sns.lineplot(x="date", y="num_tts", data=df_num_tts)
sns_plot.set(xticks=range(0, df_num_tts.shape[0], 5))
sns_plot.set(xlabel="Data", ylabel = "Número de tweets")
fig = sns_plot.get_figure()
fig.savefig("twitter_count.png")
