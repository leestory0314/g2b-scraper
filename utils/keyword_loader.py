def load_keywords(path="keywords.txt"):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
