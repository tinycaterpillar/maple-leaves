import requests

def get_english_definitions(word):
    """
    주어진 영어 단어의 영영 정의 목록을 반환
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        definitions = []

        # 각 품사별 의미 추출
        for meaning in data[0].get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "")
            for d in meaning.get("definitions", []):
                definition = d.get("definition", "")
                if definition:
                    definitions.append(f"({part_of_speech}) {definition}")
        return definitions
    else:
        return [f"No definition found for '{word}' (status: {response.status_code})"]

if __name__ == "__main__":
    word = "adsf"
    defs = get_english_definitions(word)
    print(f"Definitions for '{word}':\n")
    for d in defs:
        print("-", d)
