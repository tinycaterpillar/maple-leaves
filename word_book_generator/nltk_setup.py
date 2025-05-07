import nltk
from nltk.data import find

def download_if_missing(resource):
    try:
        find(resource)
    except LookupError:
        nltk.download(resource.split('/')[-1])

def setup_nltk():
    download_if_missing('corpora/wordnet')
    download_if_missing('corpora/stopwords')
    download_if_missing('corpora/omw-1.4')
    download_if_missing('tokenizers/punkt')
    download_if_missing('taggers/averaged_perceptron_tagger_eng')
