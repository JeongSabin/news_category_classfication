from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    # url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'

    resp = requests.get(url, headers=headers)
    # print(resp)

    soup = BeautifulSoup(resp.text, 'html.parser')  # html 형태로 parsing 하라는 뜻이다
    # print(soup)

    title_tags = soup.select('.cluster_text_headline')
    print(title_tags[0].text)

    titles = []
    for title_tag in title_tags:
        title = re.compile('[^가-힣 ]').sub('',title_tag.text)   # 가-힣 과 띄어쓰기를 빼고 제외한다 그리고 그 자리를 ''로 채워넣어라
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                          ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
# df_titles.to_csv('./crawling_data/naver_headline_news{}.csv'.format(
#     datetime.datetime.now().strftime('%y%m%d'), index=False
# ))