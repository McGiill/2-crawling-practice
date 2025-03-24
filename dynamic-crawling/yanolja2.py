from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = 'https://www.yanolja.com/reviews/domestic/10040392'

driver.get(url)
time.sleep(3)


scroll_count = 10  # 스크롤 횟수 설정
for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1) 

from bs4 import BeautifulSoup

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')


reviews_class = driver.find_elements(By.CSS_SELECTOR,".content-text.css-c92dc4")
reviews = []

# 각 리뷰 텍스트 정리 후 추가
for review in reviews_class:
    cleaned_text = review.text.strip().replace('\r', '').replace('\n', '')
    reviews.append(cleaned_text)

reviews


# 별점 추출
ratings = []
rating_containers = driver.find_elements(By.CSS_SELECTOR,".css-rz7kwu")


# 각 리뷰별로 별점 계산
for container in rating_containers:
    stars = container.find_elements(By.CSS_SELECTOR, "svg.css-1mj121y")
    rating = len(stars) 
    ratings.append(rating)

ratings


import pandas as pd

# 별점과 리뷰를 결합하여 리스트 생성
data = list(zip(ratings, reviews))

# DataFrame으로 변환
df_reviews = pd.DataFrame(data, columns=['Rating', 'Review'])
df_reviews


average_rating = sum(ratings) / len(ratings)
average_rating


from collections import Counter
import re

# 불용어 리스트 (한국어)
korean_stopwords = set(['이', '그', '저', '것', '들', '다', '을', '를', '에', '의', '가', '이', '는', '해', '한', '하', '하고', '에서', '에게', '과', '와', '너무', '잘', '또','좀', '호텔', '아주', '진짜', '정말'])

# 모든 리뷰를 하나의 문자열로 결합
all_reviews_text = " ".join(reviews)

# 단어 추출 (특수문자 제거)
words = all_reviews_text.split()  # 띄어쓰기 기준 분리
words = [re.sub(r"[^가-힣]", "", word) for word in words if re.sub(r"[^가-힣]", "", word)]

# 불용어 제거
filtered_words = [word for word in words if word not in korean_stopwords]

# 단어 빈도 계산
word_counts = Counter(filtered_words)

# 자주 등장하는 상위 15개 단어 추출
common_words = word_counts.most_common(15)



# 분석 결과 요약
summary_df = pd.DataFrame({
    'Average Rating': [average_rating],
    'Common Words': [', '.join([f"{word}({count})" for word, count in common_words])]
})

# 최종 DataFrame 결합
final_df = pd.concat([df_reviews, summary_df], ignore_index=True)
print(final_df)

# Excel 파일로 저장
######## your code here ########
final_df.to_excel('yanolja2.xlsx',index=False)
