# utils/keyword_loader.py
def load_keywords():
    with open("keywords.txt", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines() if line.strip()]
    return keywords
