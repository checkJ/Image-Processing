import cv2
import os
import time

#処理したい動画の数
f = 20


start = time.time()
cd = os.getcwd()

for a in range(f):
    # 読み込む動画の長さとfpsの設定値を入力
    file_name = str(a)+".mp4"

    # カレントディレクトリ情報の取得

    file_path = os.path.join(cd, "source", file_name)



    # 動画の読み込み。ここで指定したインスタンスが以降の動画操作系のコマンドに継承されていく
    cap = cv2.VideoCapture(file_path)

    # スクリーンキャプチャを保存するdirectory設定
    dir_name = str(a)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    save_path = os.path.join(cd, dir_name)

    # 動画のフレーム数を確認。のちのforループで使用するのでint型に指定
    frame_count = int(cap.get(7))

    # フレームを連番画像として保存
    for i in range(frame_count):
        ret, frame = cap.read()
        cv2.imwrite("%s/snap_%d%05d.png" % (save_path, a, i), frame)


#動画の長さと処理時間の関係
end = time.time() - start



print("%s 秒かかりました"%end)
