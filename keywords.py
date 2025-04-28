def load_keywords(filepath="keywords.txt"):
    with open(filepath, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
