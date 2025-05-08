from collections import Counter
from wordfreq import word_frequency
from filters import is_study_friendly, is_meaningful, lemmatize_word
from text_loader import extract_words
from nltk.corpus import wordnet
from cefr_data import CEFR_DICT
from googletrans import Translator

translator = Translator()

def translate_word(word):
    try:
        translated = translator.translate(word, src='en', dest='ko')
        translated_meaning = translated.text
        synsets = wordnet.synsets(word)
        
        if not synsets: raise ValueError("No synsets found")
        
        s = synsets[0]  # 가장 일반적인 의미
        return f"({s.pos()}) {translated_meaning}"
    except Exception as e:
        return "번역에 실패했습니다."
    

def get_nltk_definitions(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return f"No definition found for '{word}' in WordNet."
    
    s = synsets[0]  # 가장 일반적인 의미
    return f"({s.pos()}) {s.definition()}"


def classify_filtered_words(text, include_english, include_korean, levels, progress_bar, progress_label):
    words = extract_words(text)
    word_counts = Counter(words)

    filtered_words = []
    for word, count in word_counts.items():
        base_word = lemmatize_word(word)

        if count < 2 or not is_study_friendly(base_word) or not is_meaningful(base_word):
            continue
        if word_frequency(base_word, 'en') > 0.001:
            continue
        level = CEFR_DICT.get(base_word, "UD")
        if level not in levels:
            continue

        filtered_words.append((base_word, level))

    # 중복 제거
    filtered_words = list(set(filtered_words))
    total = len(filtered_words)
    processed = 0
    last_percent = -1

    level_buckets = {level: [] for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'UD']}

    for base_word, level in filtered_words:
        if level in levels:
            row = [base_word]
            if include_english:
                row.append(get_nltk_definitions(base_word))
            if include_korean:
                row.append(translate_word(base_word))
            level_buckets[level].append(row)

        # ✅ 진행률 표시 (5% 단위)
        processed += 1
        percent = int((processed / total) * 100)
        if percent // 5 > last_percent // 5:
            last_percent = percent
            progress_bar.after(0, lambda p=percent: progress_bar.config(value=p))
            progress_label.after(0, lambda p=processed: progress_label.config(
                text=f"[번역 중] {p} / {total} 단어 번역됨"))

    # ✅ 최종 완료 상태 표시
    progress_bar.after(0, lambda: progress_bar.config(value=100))
    progress_label.after(0, lambda: progress_label.config(
        text=f"[번역 완료] {processed} / {total} 단어"))

    return level_buckets