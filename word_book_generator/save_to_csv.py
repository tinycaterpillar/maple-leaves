import os
from openpyxl import Workbook


def save_each_level_to_excel(level_buckets, include_english, include_korean, levels, save_folder=None):
    if save_folder is None:
        save_folder = os.getcwd()

    for level in levels:
        word_list = level_buckets.get(level, [])
        if not word_list:
            continue

        filename = os.path.join(save_folder, f"word_book_{level}.xlsx")
        wb = Workbook()
        ws = wb.active
        ws.title = f"Level {level}"

        # ✅ 헤더 구성
        header = ["단어"]
        if include_english:
            header.append("영어 뜻")
        if include_korean:
            header.append("한글 뜻")
        ws.append(header)

        for entry in word_list:
            word = entry[0]
            idx = 1
            row = [word]

            if include_english:
                row.append(entry[idx])
                idx += 1
            if include_korean:
                row.append(entry[idx])

            ws.append(row)
        wb.save(filename)
        print(f"✅ Saved: {filename}")