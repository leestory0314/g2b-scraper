import requests

rss_url = "https://www.g2b.go.kr/rss/news/ptNewsRss.jsp?taskClCd=5"
response = requests.get(rss_url)

print("✅ RSS 상태 코드:", response.status_code)
print("✅ 응답 길이:", len(response.text))

# 상위 500자만 출력
print("📄 응답 내용 일부:")
print(response.text[:500])
