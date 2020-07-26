# -*- coding: utf-8 -*-
# Grpcモジュールのインポート
from grpc.tools import protoc

# 生成オプション
protoc.main(
    (
        '',
        '-I.',
        '--python_out=.', #書き出し先指定
        '--grpc_python_out=.', #書き出し先指定
        './Datas.proto' #書き出し元のファイル指定
    )
)
