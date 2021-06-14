# -*- coding: utf-8 -*-
"""
크롬 드라이버 설치 이후 driver에 설치 경로 입력
꼭!!☆현재 크롬 버전☆에 맞게 설치해주셔야 합니다!
크롬 버전이 91.0.4472.19인 경우(크롬 최신 업데이트(21/6/14 기준))
https://chromedriver.storage.googleapis.com/index.html?path=90.0.4430.24/

크롬 버전이 91.0.4472.19가 아닌 경우,
https://sites.google.com/a/chromium.org/chromedriver/downloads
에서 맞는 버전을 찾아 chromedriver다운로드
* 이 프로젝트 버전 : 91.0.4472.19
--------------------------------------------------

★ pip install gensim==3.8.1
- Gensim package version을 3.8.1로 해주어야 에러가 발생하지 않는다.
참고 사이트 : https://stackoverflow.com/questions/66952438/attributeerror-cant-get-attribute-vocab-on-module-gensim-models-word2vec

---------------------------------------------------

pre-trained word vector 모델 ko.bin 다운(https://github.com/Kyubyong/wordvectors)
https://drive.google.com/file/d/0B0ZXk88koS2KbDhXdWg1Q2RydlU/view

---------------------------------------------------
라이브러리 설치 
> pip install selenium
> pip install bs4
> pip install openpyxl
> pip install lxml
> pip install gensim==3.8.1

"""
#경로 입력해주세요.
chrome_driver_PATH = 'chromedriver91.exe'
stopwords_file_PATH = 'stopwords.txt' 
model_PATH = './ko.bin'

import konlpy, time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from gensim.models import Word2Vec
from collections import Counter

def youtube_loading(chrome_driver_PATH, url):
    #크롬 창만 안띄우기
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=ko_KR')
    
    print("유튜브 링크에 접속 중 입니다. 잠시만 기다려 주세요...")
    driver = wd.Chrome(executable_path = chrome_driver_PATH, options= chrome_options)

    print("댓글을 수집 중 입니다. 잠시만 기다려 주세요...")
    
    driver.get(url)
    
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    n = 0
    while True:
        n+=1
        if n%5==0:
            print("댓글을 수집 중 입니다. 잠시만 기다려 주세요...")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.0)       # 인터발 1이상으로 줘야 데이터 취득가능(롤링시 데이터 로딩 시간 때문)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
    
    html_source = driver.page_source
    driver.close()
    return html_source

def tag_crawling(html_source):
    # HTML 태크 크롤링 작업
    soup = BeautifulSoup(html_source, "lxml")
    
    youtube_comments = soup.select("div#content > yt-formatted-string#content-text") # A#B(A는 태그 값, B는 id 값)
    youtube_comments_counts = soup.select("h2#count > yt-formatted-string > span" )
    youtube_title = soup.select("div#container > h1 > yt-formatted-string") # title style-scope ytd-video-primary-info-renderer
    youtube_title = youtube_title[0].text
    return youtube_comments, youtube_comments_counts, youtube_title
  
def processing_comments():
    str_youtube_comments_all = []  # 전체 댓글 내용 배열
    for i in range(len(youtube_comments)):
        str_tmp = str(youtube_comments[i].text)    
        str_tmp = re.sub('\n', '', str_tmp)
        str_tmp = re.sub('\t', '', str_tmp)
        str_tmp = re.sub('   ', '', str_tmp)
        str_youtube_comments_all.append(str_tmp)
    return str_youtube_comments_all
    
def korean_comment_extract():
    str_youtube_comments_ko = [] # 한글 댓글 내용 배열
    for i in range(len(str_youtube_comments_all)):
        if(re.search('[가-힣ㄱ-ㅎㅏ-ㅣ]+',  str_youtube_comments_all[i])):
            str_youtube_comments_ko.append( str_youtube_comments_all[i])
    return str_youtube_comments_ko

def sub_other_language():
    #한글만 골라내기
    comments_word = []
    for i in range(len(str_youtube_comments_ko)): 
            #ㄱ-ㅎ이나 ㅏ-ㅣ같은 모음이나 자음으로만 이루어 진 것도 제
            comments_word.append(re.sub('[^가-힣 ]', '', str_youtube_comments_ko[i]))
    return comments_word

def POS_tagging():           
    # POS tagging
    pos_tagging = []
    for i in range(len(comments_word)):
        pos_tagging.append(Okt.pos(comments_word[i]))   
    return pos_tagging  

#명사만 추출(불용어 제거)
def noun_extract():  
    noun_list = []
    # list에 명사인건 추가, 불용어는 제거
    for i in range(len(pos_tagging)):
        for word,tag in pos_tagging[i]:
            if tag in ['Noun'] and word not in stopwords:
                noun_list.append(word)
    return noun_list

def get_similarity():
    similarity = []
    for i in range(len(Common_words)):
        for j in range(len(vocabs)):
            try:
                similarity.append((Common_words[i][0], vocabs[j], word_vectors.similarity(Common_words[i][0], vocabs[j])))
            except: #예외 처리
                continue 
    #유사도 순으로 정렬
    similarity.sort(key = lambda x:-x[2])
    return similarity

def delete_high_similarity(similarity):
    similarity_high = [] #유사도 0.9 이상인 단어 모을 리스트 
    for i in similarity: 
            if i[2] > 0.9: #유사도가 0.9이상인 단어 추가
                similarity_high.append(i)            
    #유사도 0.9 이상인 단어는 지운다.(거의 같은 단어에 가깝기때문)
    for i in similarity_high:
        similarity.remove(i)
    return similarity

 
# INPUT YOUTUBE URL
url = input("유튜브 링크를 입력해주세요 : ") # 댓글 수집할 Youtube URL입력

#유튜브 접속
html_source = youtube_loading(chrome_driver_PATH, url)
#댓글 수집
youtube_comments, youtube_comments_counts, youtube_title = tag_crawling(html_source)

#총 댓글 개수 출력
print("총 ", end = "")
for i in range(len(youtube_comments_counts)):
    print(youtube_comments_counts[i].text, end = " ")   
print()

#불필요한 텍스트 제거(\n,\t 등)
str_youtube_comments_all = processing_comments()

#한글 댓글만 추출
str_youtube_comments_ko = korean_comment_extract() 

print("수집된 총 한글 댓글 개수 :" , len(str_youtube_comments_ko), "개")

'''
#한글댓글 출력
for i in range(len(str_youtube_comments_ko)): 
    print(str_youtube_comments_ko[i])
'''
#한글 댓글에 섞여있는 다른언어 제거
comments_word = sub_other_language()

#토큰화
Okt = konlpy.tag.Okt()
stopwords = open(stopwords_file_PATH, 'rt', encoding='UTF8').read() # 불용어 모음 파일 불러오기
stopwords = stopwords.split(' ')

pos_tagging = POS_tagging()
noun_list = noun_extract()
            
#카운트 순 정렬, 상위 20개 정도만 뽑음
#상위 20개 단어와 높은 유사도를 가진 단어 50개를 추출한다.
counts = Counter(noun_list)
Common_words = counts.most_common(30)

model = Word2Vec.load(model_PATH)
word_vectors = model.wv #단어 벡터
vocabs = list(word_vectors.vocab.keys()) #로드한 모델에서 단어만 뽑아서 리스트로 만든다.

similarity = delete_high_similarity(get_similarity())

word1_to_excel = [] #엑셀 파일에 넣을 리스트, 빈도수 TOP30
word2_to_excel = [] #엑셀 파일에 넣을 리스트, 유사도 TOP100 
print('\n----------------------------------------------------------\n')
print("빈도수 순 상위 30개 단어 출력 : ")
for i in Common_words:
    print(i[0] , end = ' ')
    word1_to_excel.append(i[0])
    
print("\n\n위 30개 단어와 유사한 단어 100개 :")
for i in similarity[:100]:
    print(i[1], end = ' ') 
    word2_to_excel.append(i[1])     
    
#엑셀 파일 만들기
korean_comment =  pd.DataFrame({'한글 댓글' : str_youtube_comments_ko}) #리스트 자료형으로 생성
countTOP30 = pd.DataFrame({'단어 빈도순': word1_to_excel})
simTOP100 = pd.DataFrame({'유사도 높은 단어' : word2_to_excel})
#korean_comment = pd.DataFrame(korean_comment) #데이터 프레임으로 전환
youtube_title = re.sub("[\/:*?\"<>|]", " ", youtube_title)
excel_name = './output/' + str(youtube_title)+' 한글댓글 모음.xlsx'

with pd.ExcelWriter(excel_name) as writer:
    korean_comment.to_excel(writer, sheet_name = '한글 댓글') #엑셀로 저장
    countTOP30.to_excel(writer, sheet_name = '빈도 TOP30 단어')
    simTOP100.to_excel(writer, sheet_name = '유사도 TOP100')