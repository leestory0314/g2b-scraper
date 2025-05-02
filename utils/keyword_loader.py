# utils/keyword_loader.py
# version: 1.0.0
# changelog:
# - v1.0.0: keyword.txt 로드 기능

def load_keywords(path="keywords.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
