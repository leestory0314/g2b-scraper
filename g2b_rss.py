import feedparser

rss_url = "https://www.g2b.go.kr/rss/news/ptNewsRss.jsp?taskClCd=5"
feed = feedparser.parse(rss_url)

print("✅ 전체 공고 10개 출력 테스트:\n")

for i, entry in enumerate(feed.entries[:10]):
    print(f"[{i+1}]")
    print("제목:", entry.get("title", "N/A"))
    print("요약:", entry.get("summary", "N/A"))
    print("날짜:", entry.get("published", "N/A"))
    print("링크:", entry.get("link", "N/A"))
    print("="*50)
