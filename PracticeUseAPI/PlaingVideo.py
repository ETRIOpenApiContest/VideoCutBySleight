import numpy as np
import cv2 as cv

videoFilePath = "/Users/sunkyu/Documents/ETRIOpenApiContest/PracticeUseAPI/videoplayback.mp4" #파일 주소

cap = cv.VideoCapture(videoFilePath)
while cap.isOpened():
  ret, frame = cap.read()

  #if frame is correctly ret is True
  if not ret:
    print("Can't receive trame (stream end?). Exiting...")
    break
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  cv.imshow('frame', gray)
  if cv.waitKey(1) == ord('q'):
    break

cap.release()
cv.destroyAllWindows()