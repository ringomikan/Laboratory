# -*- coding: utf-8 -*-
#============================================================
# import packages
#============================================================
#必要パッケージのインポート
from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import Datas_pb2
import Datas_pb2_grpc
import sys

#============================================================
# class
#============================================================

#============================================================
# property
#============================================================

#============================================================
# functions
#============================================================
def run():

    # アクセス先を指定、今回はローカルにサーバーが立つのでローカルIPを指定する
    channel = grpc.insecure_channel('127.0.0.1:50051')

    # スタブ
    stub = Datas_pb2_grpc.MainServerStub(channel)


    while True:
        try:


            message = []
            message.append(Datas_pb2.Request(msg = 'give me the stream!!'))

            # サーバーにリクエストを投げてレスポンスを取得
            responses = stub.getStream(iter(message))


            for res in responses:

                # print(res)

                # 元データがbase64になっているのでデコードする
                b64d = base64.b64decode(res.datas)

                # バイナリデータをuint8形式に変換
                dBuf = np.frombuffer(b64d, dtype = np.uint8)

                # cv2で扱えるように更に変換
                dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
                #print("dst size : ", sys.getsizeof(dst))


                cv2.imshow('Capture Image', dst)

                k = cv2.waitKey(1)
                if k == 27:
                    break

        # 何かしらのエラーがあった場合はプリント
        except grpc.RpcError as e:
            print(e.details())
            #break


#============================================================
# Awake
#============================================================

#============================================================
# main
#============================================================
if __name__ == '__main__':
    run()

#============================================================
# after the App exit
#============================================================
cv2.destroyAllWindows()
