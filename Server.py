# -*- coding: utf-8 -*-
#============================================================
# import packages
#============================================================
#必要パッケージのインポート
from concurrent import futures
import grpc
import Datas_pb2
import Datas_pb2_grpc
import time
import cv2
import base64
import sys
from picamera import PiCamera
import numpy as np
import io
stream = io.BytesIO()
camera = PiCamera()
camera.resolution = (1024, 768)

#============================================================
# property
#============================================================
#カメラ情報の取得、準備
"""
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
"""
#キャプチャデータ確保用の変数
captureBuffer = None


#============================================================
# class
#============================================================
# .protoを使って生成したクラスを継承して、独自のメソッドを持たせたサーバーを用意
class Greeter(Datas_pb2_grpc.MainServerServicer):

    #==========
    def __init__(self):
        pass

    #==========
    def getStream(self, request_iterator, context):

        for req in request_iterator:

            # リクエストメッセージのプリント
            print("request message = ", req.msg)

            # なんとなくグレイスケールにする
            gray = cv2.cvtColor(captureBuffer, cv2.COLOR_BGR2GRAY)

            # 画像をjpg形式にする
            ret, buf = cv2.imencode('.jpg', gray)
            if ret != 1:
                return

            # base64形式にエンコード
            b64e = base64.b64encode(buf)
            # print("base64 encode size : ", sys.getsizeof(b64e))

            # クライアントにデータを返す
            yield Datas_pb2.Reply(datas = b64e)



#============================================================
# functions
#============================================================
def serve():

    # スレッドを用いてサーバーを起動、同時アクセス数は10に制限
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))

    # 先ほど作ったGreeterクラスを引数にする
    Datas_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)

    # ポート番号を指定
    server.add_insecure_port('[::]:50051')

    # サーバースタート
    server.start()

    print('server start')

    while True:
        try:
            camera.capture(stream, format='jpeg')
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, 1)

            # キャプチャデータを格納する
            global captureBuffer
            captureBuffer = image

            #cv2.imshow('image',captureBuffer)
            k = cv2.waitKey(1)
            if k == 27:
                break

            time.sleep(0)

        except KeyboardInterrupt:
            server.stop(0)



#============================================================
# main
#============================================================
if __name__ == '__main__':
    serve()


#============================================================
# after the App exit
#============================================================
cap.release()
cv2.destroyAllWindows()
