
import cv2


# haarcascade 불러오기
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# 이미지 불러오기
original_num = 2
img = cv2.imread(str(original_num)+'.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



# 얼굴인식 및 인식개수가 1개 초과 시 종료(나중에 반복문으로 리턴 구현)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

if (len(faces)==1):
    for (x, y, w, h) in faces:
        cropped = img[y - int(h / 4):y + h + int(h / 1), x - int(w / 4):x + w + int(w / 4)]  # 상:하, 좌:우
else:
    print("얼굴 다중인식")
    exit()


# 자른 사진 크기 조정 #게임 IF 이미지 크기: 400, 500
if cropped.shape[1]*cropped.shape[0]>2000:
    resize_img = cv2.resize(img, dsize=(400, 500), interpolation=cv2.INTER_AREA)
else:
    resize_img = cv2.resize(img, dsize=(400, 500), interpolation=cv2.INTER_CUBIC)


# 자른 사진 저장
change_num = 99
cv2.imwrite(str(change_num)+".jpg",cropped)


# 원본 사진, 자른 사진 출력
cv2.imshow('image', img)
cv2.imshow("cropped", cropped)

key = cv2.waitKey(0)
cv2.destroyAllWindows()
