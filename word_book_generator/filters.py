import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def is_meaningful(word):
    if word in stop_words:
        return False
    if len(word) <= 2:
        return False
    if not wordnet.synsets(word):
        return False
    return True

def is_study_friendly(word):
    tag = nltk.pos_tag([word])[0][1]
    excluded_tags = {
        'DT', 'IN', 'CC', 'PRP', 'PRP$', 'WDT', 'WP', 'WP$', 'WRB'
    }
    return tag not in excluded_tags

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatize_word(word):
    pos = nltk.pos_tag([word])[0][1]
    wn_pos = get_wordnet_pos(pos)
    return lemmatizer.lemmatize(word, pos=wn_pos)