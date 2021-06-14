# 유튜브 다음 콘텐츠 구상 프로젝트(korean.ver)

## 🎈프로젝트 개요

유튜브를 즐겨보는 한국인이라면 다음과 같은 댓글을 본 적이 있을 것입니다.

>축하합니다! 당신은 한국인을 발견했습니다!

한국영상인데도 불구하고 외국 댓글이 대부분을 차지하여 한글 댓글을 찾기 힘든 경우가 종종 있습니다. 이처럼 유튜브 외국어 댓글 속 한글 댓글만 찾아 보고 싶을 때가 있어 이 프로젝트를 구상하게 되었습니다.

 한글 댓글만 볼 수 있는 것으로 마친다면, 너무 단순한 프로젝트가 될 것 같아 추출한 댓글로 할 수 있는 추가 기능을 생각해보았습니다.

 추출한 댓글에서 단어(명사)만 추출, 빈도 수가 높은 단어를 통해 해당 영상에서 어떤 반응이 가장 많은지 탐색할 수 있습니다.
 또한 이 단어들과 유사한 단어들을 추출하여 유튜브 크리에이터가 다음 영상 콘텐츠 주제를 쉽게 생각해 낼 수 있도록 유도합니다.

---

 ## ✏프로젝트 기능

1. 유튜브 댓글에서 한글 댓글 추출
2. 단어 빈도순 상위 30개 추출
3. 상위 30개 단어와 유사 단어 100개 추출
    - 미리 학습된 모델 사용 https://drive.google.com/file/d/0B0ZXk88koS2KbDhXdWg1Q2RydlU/view
4. 한글댓글, 추출 단어 엑셀 파일 생성 

---

## 📂사용방법
- youtube_comments_SourceCode.py 실행

크롬 드라이버 설치 이후 chrome_driver_PATH에 설치 경로 입력

꼭!!**☆현재 크롬 버전☆**에 맞게 설치해주셔야 합니다!

- 크롬 버전이 91.0.4472.19인 경우

    (크롬 최신 업데이트(21/6/14 기준))
https://chromedriver.storage.googleapis.com/index.html?path=90.0.4430.24/

- 크롬 버전이 91.0.4472.19가 아닌 경우,
https://sites.google.com/a/chromium.org/chromedriver/downloads
에서 맞는 버전을 찾아 chromedriver다운로드

* 이 프로젝트 chrome driver 버전 : 91.0.4472.19

-----------------

 <span style="color:red">★</span> **pip install gensim==3.8.1**<span style="color:red">★</span>
- Gensim package version을 3.8.1로 해주어야 에러가 발생하지 않는다.

    참고 사이트 : https://stackoverflow.com/questions/66952438/attributeerror-cant-get-attribute-vocab-on-module-gensim-models-word2vec

---

pre-trained word vector 모델 **ko.bin** 다운( 출처 : https://github.com/Kyubyong/wordvectors)

이미 레포지토리 안에 들어 있긴 합니다!

다운 링크 🔽

https://drive.google.com/file/d/0B0ZXk88koS2KbDhXdWg1Q2RydlU/view

---

라이브러리 설치 
> pip install selenium

> pip install bs4

> pip install openpyxl

> pip install lxml

> pip install gensim==3.8.1

---
## 🎁프로젝트 결과
test용 영상 링크 : https://www.youtube.com/watch?v=H0Ds7z95CvM

- 댓글 리스트
    > 봄소풍 가야겠어요~go picnic~

    > 벚꽃의 꽃말은 중간고사

    > 벚꽃 예쁘다ㅎㅎㅎ

    > ohhh its so wonderful

    > 봄이네요~

    > oh 예뻐요 oh

### 📈최종 결과물

### 1) output
![image](https://user-images.githubusercontent.com/28985207/121910124-8c0f3880-cd69-11eb-8a39-35f22da1c420.png)

### 2) excel 파일(.xlxs)
* 제목 : 영상 타이틀 + 한글 댓글모음.xlxs

* 3개의 sheet : 한글댓글, TOP30 단어, TOP100 유사도

 >>> ![image](https://user-images.githubusercontent.com/28985207/121889829-a5f25080-cd54-11eb-98a2-e45eba7093ab.png)


* 자세한 구조는 output 폴더 안 '벚꽃잎 폭풍 한글댓글 모음' 파일 참조
---
## 😥한계점

- 인물의 이름이 자주 나타날 경우, 유사도 높은 단어로 인물의 이름이 꽤나 많이 나타나는 문제가 있다.
- 동물, 가족 호칭(오빠, 언니 등)도 마찬가지
- 가족 호칭은 상대적으로 적어 stopwords 파일에 추가하여 어느 정도 해결

---
 ## 🧾참조
 <br>
 PythonSelenium을-사용하여-유튜브-댓글-가져오기 

 > https://somjang.tistory.com/entry/PythonSelenium%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EB%8C%93%EA%B8%80-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0
 
 POS tagging 및 카운트 정렬 
 > https://knowable.tistory.com/5

 미리 학습된 Word2Vec 모델 
 > https://github.com/Kyubyong/wordvectors
 
 >모델 다운 https://drive.google.com/file/d/0B0ZXk88koS2KbDhXdWg1Q2RydlU/view

 파이썬 데이터 엑셀 파일 저장 
 > https://ponyozzang.tistory.com/619

 불용어 파일 내용 참조
  > https://mr-doosun.tistory.com/24

 <br>
  
  \*  본 프로젝트는 서울과학기술대학교 컴퓨터공학과 2021-1학기 자연어처리 강좌 프로젝트 과제물로 사용하였습니다. \*

  github 업로드(예정) : https://github.com/dmswl9898/YouTube_Korean_comments_count-similarity
