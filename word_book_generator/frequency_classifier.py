from collections import Counter
from wordfreq import word_frequency
from filters import is_study_friendly, is_meaningful, lemmatize_word
from text_loader import extract_words
import csv
from nltk.corpus import wordnet
from tqdm import tqdm
from cefr_data import CEFR_DICT

def get_nltk_definitions(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return f"No definition found for '{word}' in WordNet."
    
    s = synsets[0]  # 가장 일반적인 의미
    return f"({s.pos()}) {s.definition()}"


def classify_filtered_words(text, min_count=2):
    words = extract_words(text)
    word_counts = Counter(words)

    # 결과를 레벨별로 저장
    level_buckets = {
        'A1': [], 'A2': [], 'B1': [], 'B2': [], 'C1': [], 'UD': []
    }

    for word, count in tqdm(word_counts.items(), total=len(word_counts)):
        base_word = lemmatize_word(word)

        if count < min_count:
            continue
        if not is_study_friendly(base_word):
            continue
        if not is_meaningful(base_word):
            continue

        freq = word_frequency(base_word, 'en')
        if freq > 0.001:
            continue

        level = CEFR_DICT.get(base_word, "UD")
        level_buckets[level].append([base_word, get_nltk_definitions(base_word)])

    return level_buckets