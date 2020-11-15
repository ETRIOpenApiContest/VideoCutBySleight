from typing import Type
import urllib3
import os
import time
import base64
import json
import moviepy.editor as mp
from pydub import AudioSegment

openApiURL = "http://aiopen.etri.re.kr:8000/VideoParse" #API호출
accessKey = "bd0d5ad2-71f3-4398-b24c-6eaddc462a05" #API접근 Key
path = r'C:\Users\skanj\Desktop\video'
video = '\movie4.mp4'

videoFilePath = path + video

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
# json파일 형식으로 다운로드
with open("fileId.json", "w") as json_file:
  json.dump(response.data.decode('utf8'), json_file)

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
# json파일 형식으로 다운로드
with open("divideResult.json", "w") as json_file:
  json.dump(response1.data.decode('utf8'), json_file)

# audio path, language, API
languageCode = "korean"
audio = "\movie4.wav"
audioFilePath = path + audio
openApiURL =  "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"

# movie to audio
clip = mp.VideoFileClip(videoFilePath)
clip.audio.write_audiofile(audioFilePath)

# audio
sound = AudioSegment.from_file(audioFilePath)

# ddd
moviedict = json.loads(response1.data.decode('utf-8'))['return_object']

#dd
split_points = []
splits = []
for i in range(1,len(moviedict['result'][0]['time'])):
    j = moviedict['result'][0]['time'][i] * len(sound)
    k = moviedict['result'][0]['time'][i-1] * len(sound)
    split_point = [k,j]
    split_points.append(split_point)

# dd
for i in range(len(split_points)):
    splits.append(sound[split_points[i][0]:split_points[i][1]])
    
# dd
for i in range(len(splits)):
    print( i, "번째 소리입니다.")
    split_audio_name = "\s" + str(i) + ".wav"
    split_audio_path = path + split_audio_name
    
    # audio split
    splits[i].export(split_audio_path, format="wav")

    # 음성인식 API 시작 앞에 5초만 나눈 오디오로 함
    file = open(split_audio_path, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
      "acces_key": accessKey,
      "argument": {
        "language_code": languageCode,
        "audio": audioContents
      }
    }

    http = urllib3.PoolManager()
    response = http.request(
      "POST",
      openApiURL,
      headers={"Content-Type": "application/json; charset=UTF-8"},
      body = json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    print(str(response.data, "utf-8")) 
    # json파일 형식으로 다운로드
    audio_file_json = "audio_file" + str(i) + ".json"
    with open(audio_file_json, "w") as json_file: 
      json.dump(response.data.decode('utf8'), json_file) 
