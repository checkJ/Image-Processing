import cv2
import os
import time

#読み込みたい動画の指定
input_file = "0.mp4"

# 動画の読み込み。ここで指定したインスタンスが以降の動画操作系のコマンドに継承されていく
cap = cv2.VideoCapture(input_file)

# スクリーンキャプチャを保存するdirectory設定
dir_name = "frame"

if not os.path.exists(dir_name):
   os.mkdir(dir_name)


cd = os.getcwd()
save_path = os.path.join(cd, dir_name)

# 動画のフレーム数を確認。のちのforループで使用するのでint型に指定
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(5)

#一つ目の変数にはフレームが読み込まれているかの確認。
#二つ目の変数には画像の配列が格納される
ret, frame = cap.read()


#読み込んだ動画の情報および一枚目を出力
print("フレーム数")
print(frame_count)
print("フレームレート")
print(fps)
print("フレーム確認")
print(ret)
cv2.imshow("1frame",frame)

cv2.waitKey(0)



# フレームを連番画像として保存
#for i in range(frame_count):
#    ret, frame = cap.read()
#    cv2.imwrite("%s/snap_%d%05d.png" % (save_path, a, i), frame)frame separate.pyframe separate.pyframe separate.py