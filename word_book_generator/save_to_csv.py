import os
import csv

def save_each_level_to_csv(level_buckets, save_foler=None):
    if save_foler is None:
        save_foler = os.getcwd()  # 현재 실행 경로

    for level, word_list in level_buckets.items():
        filename = os.path.join(save_foler, f"word_book_{level}.csv")
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for word, meaning in word_list:
                writer.writerow([word, meaning])
        print(f"✅ Saved: {filename}")
