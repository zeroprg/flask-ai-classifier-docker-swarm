import requests
import cv2
import numpy as np
import os.path
import imutils
import re

class VideoStream:
    def __init__(self, url):
        self.url = url
        self.cap = None

        if "jpg" in url:
            self.cap = self._create_jpg_cap(url)
        elif "/cgi-bin/" in url:
            self.cap = self._create_cgi_bin_cap(url)
        elif  bool(re.search(r'.*\.(?!mjpg)(jpg|jpeg|png|gif|bmp)\b|\b[jJ][pP][eE]?[gG]\b|\bSnapshot\b|/image/', url, re.IGNORECASE)):
            frame = imutils.url_to_image(self.url)
            self.cap = cv2.VideoCapture()
        elif ".h264" in url:
            self.cap = self._create_h264_cap(url)
        else:
            raise ValueError("Unsupported video stream URL")

    def _create_jpg_cap(self, url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return cap

    def _create_cgi_bin_cap(self, url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
        return cap

    def _create_h264_cap(self, url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return cap

    def read(self):
        if self.cap is None:
            raise ValueError("Video stream not initialized")

        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            raise ValueError("Failed to read frame from video stream")

    def read_from_url(self, url):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                content += chunk
                a = content.find(b'\xff\xd8')
                b = content.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = content[a:b+2]
                    content = content[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    return frame
        else:
            raise ValueError("Failed to read frame from video stream")


# Test case
stream_url =  "http://194.44.38.196:8083/mjpg/video.mjpg" # "http://119.106.70.133:8083/?action=stream" "http://150.129.120.142:84/cgi-bin/snapshot.cgi?chn=0&u=admin&p=&q=0&COUNTER"
vs = VideoStream(stream_url)

try:
    while True:
        frame = vs.read_from_url(stream_url)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print(f"Error reading video stream: {e}")

vs.cap.release()
cv2.destroyAllWindows()




