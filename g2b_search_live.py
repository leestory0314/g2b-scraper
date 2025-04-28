before = driver.current_url
driver.execute_script("arguments[0].click();", link)  # 입찰공고목록
time.sleep(3)
after = driver.current_url

print(f"🔍 클릭 전 URL: {before}")
print(f"🔍 클릭 후 URL: {after}")
