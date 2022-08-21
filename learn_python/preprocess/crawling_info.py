INFO = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def load_problem_url():
    with open("../source/problemURL.ktx", 'r+', encoding='utf-8') as f:
        ret = set(map(lambda x: x.strip(), f.readlines()))

    return ret