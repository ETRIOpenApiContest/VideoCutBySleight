'''홈페이지 구현예제_1(20201106) by Python3#'''
 # -*- coding:utf-8 -*-
import urllib3
import json
import os

openApiURL = "http://aiopen.etri.re.kr:8000/VideoParse" #API호출
accessKey = "16f35e3e-b273-4953-9366-4c7d68128530" #API접근 Key
videoFilePath = "/Users/sunkyu/Documents/ETRIOpenApiContest/PracticeUseAPI/UsingSleight.mp4" #파일 주소

file = open(videoFilePath,'rb') #파일 열기 (이진파일 읽기 권한부여)
fileContent = file.read()
file.close()

requestJson = {
  "access_key": accessKey,
  "argument":{}
}

http = urllib3.PoolManager()

response = http.request(
  "POST",
  openApiURL,
  fields={
    'json':json.dumps(requestJson),
    'uploadfile':(os.path.basename(file.name), fileContent)
  }
)

print("[responseCode]" + str(response.status))
print("[responBody")
print(response.data)

