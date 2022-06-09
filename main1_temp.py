from selenium import webdriver
import os
import urllib.request
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
import time

chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")


# haarcascade 불러오기
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


header_n = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

def crawl(keywords):

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    path = "https://www.google.com/search?q=" + keywords + "&newwindow=1&rlz=1C1CAFC_enKR908KR909&sxsrf=ALeKk01k_BlEDFe_0Pv51JmAEBgk0mT4SA:1600412339309&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj07OnHkPLrAhUiyosBHZvSBIUQ_AUoAXoECA4QAw&biw=1536&bih=754"
    driver = webdriver.Chrome('./chromedriver',options=options)
    driver.get(path)

    counter = 0
    succounter = 0

    # data 디렉토리 없으면 만들기
    if not os.path.exists('data'):
        os.mkdir('data')
    #if not os.path.exists('data/' + keywords):
        #os.mkdir('data/' + keywords)

    for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'):
        counter = counter + 1
        #print(counter)
        # 이미지 url
        img = x.get_attribute("data-src")
        if img is None:
            img = x.get_attribute("src")
        #print(img)

        # 이미지 확장자
        imgtype = 'jpg'

        # 구글 이미지를 읽고 저장한다.

        raw_img = urllib.request.urlopen(img).read()

        # 바이너리 타입을 행렬 이미지 형식으로 변환
        # raw_img = np.frombuffer(raw_img, dtype=np.uint8)

        File = open(os.path.join('data/', keywords + "_" + str(counter) + "." + imgtype), "wb")
        File.write(raw_img)
        File.close()

        path = 'data/' + keywords + "_" + str(counter) + "." + imgtype

        # 얼굴 인식 및 사진 자르고 저장

        img_array = np.fromfile(path, np.uint8)  # 컴퓨터가 읽을수 있게 넘파이로 변환
        decode_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 이미지를 읽어옴

        # gray = cv2.cvtColor(decode_img, cv2.COLOR_BGR2GRAY)

        # temp_img = cv2.imread('data/' + keywords + "_" + str(counter) + "." + imgtype)

        # cv2.imshow('img', curImg)

        faces = face_cascade.detectMultiScale(decode_img, 1.3, 5)
        if len(faces) == 1:  # 성공적 인식
            for (x, y, w, h) in faces:
                cropped_img = decode_img[y - int(h / 4):y + h + int(h / 1), x - int(w / 4):x + w + int(w / 4)]  # 상:하, 좌:우

                # 자른 사진 크기 조정 #게임 IF 이미지 크기: 400, 500(400, 500)
                resized_img = cv2.resize(cropped_img, dsize=(400, 500), interpolation=cv2.INTER_CUBIC)

                extension = os.path.splitext(keywords + "_" + str(counter) + "." + imgtype)[1]

                # 자른 사진 저장
                result, encoded_img = cv2.imencode(extension, resized_img)

                if result:
                    with open('data/' + keywords + "_" + str(counter) + "." + imgtype, mode='w+b') as f:
                        encoded_img.tofile(f)

            succounter = succounter + 1
            break

        else:  # 다중인식
            print("얼굴 다중인식\n")
            os.remove('data/' + keywords + "_" + str(counter) + "." + imgtype)  # 다중인식한 사진은 삭제처리

        if counter == 3:
            break

    print(succounter, "succesfully downloaded")
    driver.close()


ulli_total = []


## 네이버 뉴스 연예 기사 크롤링함수
def newsCrawling():
    url = 'https://entertain.naver.com/home'
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    titles_html = soup.select('.title_area > a')
    txt_area = soup.select('.txt_area > a')

    f = open("news.txt", 'w', encoding='UTF-8')

    for i in range(len(titles_html)):
        # print(i+1, titles_html[i].text)
        f.write(titles_html[i].text)

    for j in range(len(txt_area)):
        # print(j+1, txt_area[j].text)
        f.write(txt_area[j].text)

    f.close()

## 위키백과 연예인 목록 크롤링 후 txt 파일로 생성
def wikiListCrawling():

    urlArray = [
                ## 남자 배우
                "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EA%B9%80%EC%83%81%ED%98%B8+%28%EB%B0%B0%EC%9A%B0%29#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EB%8F%99%EC%9C%A4%EC%84%9D#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%84%9C%EC%98%81%EC%A3%BC#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%98%A4%EC%84%B1%EC%97%B4#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%9D%B4%EC%8A%B9%EC%9D%BC+%28%EB%B0%B0%EC%9A%B0%29#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%A0%84%EB%B3%91%EC%9A%B1+%28%EB%B0%B0%EC%9A%B0%29#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%B5%9C%EA%B1%B4%EC%9A%B0#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%ED%99%A9%EB%A7%8C%EC%9D%B5#mw-pages",
                ## 여자 배우
                "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EA%B9%80%EC%9D%B4%EC%A7%80#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EB%B0%95%ED%95%9C%EB%B3%84#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%96%91%ED%98%84%EC%98%81#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%9D%B4%EC%8B%9C%EC%9A%B0+%281997%EB%85%84%29#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%EC%A0%95%EC%88%98%EC%A7%80#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%EB%B0%B0%EC%9A%B0&pagefrom=%ED%95%9C%EB%8B%A4%EC%9D%80#mw-pages",
                ## 아이돌
                "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%95%84%EC%9D%B4%EB%8F%8C",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%95%84%EC%9D%B4%EB%8F%8C&pagefrom=%EC%84%B1%EB%AF%BC+%281986%EB%85%84%29#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%95%84%EC%9D%B4%EB%8F%8C&pagefrom=%EC%A1%B0%EC%8B%9C%EC%9C%A4#mw-pages",
                ## 남자 희극인
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%ED%9D%AC%EA%B7%B9%EC%9D%B8&pageuntil=%EC%9D%B4%ED%98%81%EC%9E%AC#mw-pages",
                "https://ko.wikipedia.org/w/index.php?title=%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EB%82%A8%EC%9E%90_%ED%9D%AC%EA%B7%B9%EC%9D%B8&pagefrom=%EC%9D%B4%ED%98%81%EC%9E%AC#mw-pages",
                ## 여자 희극인
                "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%97%AC%EC%9E%90_%ED%9D%AC%EA%B7%B9%EC%9D%B8"
    ]

    for t in range(0,21):
        html = urlopen(f"{urlArray[t]}")
        bsObject = BeautifulSoup(html, "html.parser")  # html 정보 가져오기
        li_code = bsObject.select('div.mw-category-group>ul>li')  # 태그까지 포함한 값이 보임

        for c in range(0, len(li_code) - 1):
            ulli_total.append(li_code[c].get_text())
        Artist = ',\n'.join(ulli_total)
        f = open("Artist.txt", 'w', encoding='UTF-8')
        f.write(Artist)
        f.close()

## news.txt와 idol.txt 문자열 비교
def check_string():
    final = [0] * (len(ulli_total)-1)
    fw = open('final.txt', 'w', encoding='UTF-8')
    with open('news.txt',encoding='UTF-8') as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        for i in range(0,len(ulli_total)-1):
            if ulli_total[i] in line:
                ## final[i] : 최종 검색 할 연예인 목록
                final[i] = ulli_total[i]
                fw.write(final[i])
                fw.write('\n')
                crawl(f"{final[i]}")

## 실행
newsCrawling()
wikiListCrawling()
check_string()
