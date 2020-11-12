import urllib3
import json
import os
import time
import cv2 as cv
import numpy as np

openApiURL = "http://aiopen.etri.re.kr:8000/VideoParse" #API호출
accessKey = "16f35e3e-b273-4953-9366-4c7d68128530" #API접근 Key
videoFilePath = "/Users/sunkyu/Documents/ETRIOpenApiContest/PracticeUseAPI/videoplayback.mp4" #파일 주소

file = open(videoFilePath,'rb')#파일 열기 (이진파일 읽기 권한부여)
fileContent = file.read()
file.close()

requestJson = { #입력 파라미터 설정
  "access_key": accessKey, #accesskey 설정
  "argument":{} #파일 입력에서는 매개변수 없음
}

http = urllib3.PoolManager() #네트워크 통신

response = http.request( #API서버에 요청
  "POST", #POST방식으로 통신
  openApiURL, #API서버 주소
  fields={ #입력 매개변수
    'json': json.dumps(requestJson),
    'uploadfile': (os.path.basename(file.name), fileContent) #파일 업로드
  }
)

print("[responseCode]" + str(response.status)) #응답코드 출력
print("[responseBody]")
print(response.data) #파일 ID 출력

time.sleep(30) #통신하는 시간 딜레이 설정

URL = openApiURL + '/status' #분석 API 서버 호출
file_id = json.loads(response.data.decode())["return_object"]["file_id"]
#file_id를 매개변수로 호출
requestJson1 = {
  "access_key": accessKey,
  "argument":{"file_id": file_id} #file_id 전송
}

http1 = urllib3.PoolManager() #API서버에 요청

response1 = http1.request( #API서버에 통신
  "POST", #POST방식으로 통신
  URL, #API 서버 주소
  fields={ #입력 매개변수
    'json': json.dumps(requestJson1),
    'uploadfile': (os.path.basename(file.name), fileContent)
  }
)

print("[responseCode]" + str(response1.status)) #응답 코드 출력
print("[responseBody]") 
print(response1.data) #장면분할 결과 출력

#############동영상 처리################
openVideo = cv.VideoCapture(videoFilePath)
frame = json.loads(response1.data.decode())
