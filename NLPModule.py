import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.stanford import StanfordTokenizer
from Structure import kmp_replace

def token_filter(str_a, word_num):
    # initialize stop_words
    stop_words = stopwords.words('english')
    stop_words = stop_words + ['!', ',', '.', '?', '-s', '-ly', '</s>', 's', '\'s', 'the', '<br', '/>', '\'', '...']
    # print("stop_words: ", stop_words)
    # tokenize & remove stop_words
    lower = str_a.lower()
    lower = remove_punctuation(lower)
    lower = kmp_replace(lower, "<br />", "")    # remove the <br /> in text
    remove = str.maketrans('', '', string.punctuation)
    removed = lower.translate(remove)
    word_token = nltk.word_tokenize(removed)
    # word_token = [word.lower() for word in word_token if word.isalpha()]
    word_num.append(len(word_token))
    return [word for word in word_token if word not in stop_words]


def token_word_count(str_a):
    lower = str_a.lower()
    lower = remove_punctuation(lower)
    lower = kmp_replace(lower, "<br />", "")  # remove the <br /> in text
    remove = str.maketrans('', '', string.punctuation)
    removed = lower.translate(remove)
    return len(nltk.word_tokenize(removed))


def stemming(filtered_words):
    # stemming
    snowball_stemmer = SnowballStemmer('english')
    stem_words = list()
    for w in filtered_words:
        stem_words.append(snowball_stemmer.stem(w))
    return stem_words


def lem(filtered_words):
    # pos & lemmatizer
    lem_words = list()
    wnl = WordNetLemmatizer()
    for word, tag in nltk.pos_tag(filtered_words):
        if tag.startswith('NN'):
            lem_words.append(wnl.lemmatize(word, pos='n'))
        elif tag.startswith('VB'):
            lem_words.append(wnl.lemmatize(word, pos='v'))
        elif tag.startswith('JJ'):
            lem_words.append(wnl.lemmatize(word, pos='a'))
        elif tag.startswith('R'):
            lem_words.append(wnl.lemmatize(word, pos='r'))
        else:
            lem_words.append(word)
    return lem_words


# make sure there's a ' ' following every '.', '?', '!'
def regulate_punctuation(str_a):
    for i in range(len(str_a)):
        if str_a[i] == '.' or str_a[i] == '!' or str_a[i] == '?':
            print(i, str_a[i:i+1])
            if i+1 < len(str_a):
                if str_a[i+1] != ' ':
                    print("find error")
                    str_a = str_a[0:i] + ' ' + str_a[i+1:]
    return str_a


def remove_punctuation(str_a):
    temp_str = ""
    for i in str_a:
        if i == ',' or i == '.' or i == '!' or i == '?':
            temp_str += ' '
        else:
            temp_str += i
    return temp_str
    """for i in range(len(str_a)):
        if str_a[i] == ',' or str_a[i] == '.' or str_a[i] == '!' or str_a[i] == '?':
            str_a = str_a[0:i] + ' ' + str_a[i+1:]"""
    return str_a

"""filtered_words = token_filter(str_a)
filtered_words = ['function', 'functional', 'functionality', 'functioning', 'functioned']
print("OG: ", filtered_words, "\n")
stem_words = stemming(filtered_words)
print("stem: ", stem_words, "\n")
lem_words = lem(filtered_words)
print("lem: ", lem_words, "\n")
temp_words = lem(lem_words)
print("2nd: ", temp_words)
dict_b = count_element(stem_words)
print("statistic: ", dict_b)
tokenizer = StanfordTokenizer()
temp_list_b = tokenizer.tokenize(str_a)"""
