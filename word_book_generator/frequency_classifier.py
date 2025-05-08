from collections import Counter
from wordfreq import word_frequency
from filters import is_study_friendly, is_meaningful, lemmatize_word
from text_loader import extract_words
from nltk.corpus import wordnet
from tqdm import tqdm
from cefr_data import CEFR_DICT
from googletrans import Translator

def get_nltk_definitions(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return f"No definition found for '{word}' in WordNet."
    
    s = synsets[0]  # 가장 일반적인 의미
    return f"({s.pos()}) {s.definition()}"


def translate_word(word):
    translator = Translator()
    try:
        translated = translator.translate(word, src='en', dest='ko')
        translated_meaning = translated.text
        synsets = wordnet.synsets(word)
        
        if not synsets: raise ValueError("No synsets found")
        
        s = synsets[0]  # 가장 일반적인 의미
        return f"({s.pos()}) {translated_meaning}"
    except Exception as e:
        return "번역에 실패했습니다."


def classify_filtered_words(text, include_english, include_korean, levels):
    words = extract_words(text)
    word_counts = Counter(words)

    level_buckets = {level: [] for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'UD']}

    for word, count in word_counts.items():
        base_word = lemmatize_word(word)

        if count < 2 or not is_study_friendly(base_word) or not is_meaningful(base_word):
            continue
        if word_frequency(base_word, 'en') > 0.001:
            continue

        level = CEFR_DICT.get(base_word, "UD")

        if level in levels:
            row = [base_word]
            if include_english:
                row.append(get_nltk_definitions(base_word))
            if include_korean:
                row.append(translate_word(word))
            level_buckets[level].append(row)
    return level_buckets