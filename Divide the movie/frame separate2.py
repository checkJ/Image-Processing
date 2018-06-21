import cv2
import os
import numpy as np
import time


global file_number,input_path,video_format

#マウスの操作のコールバック関数
def mouse_callback(event, x, y, flags, param):

    global input, img_win, sx, sy, rect, abs_x, abs_y, abs_sx, abs_sy
    abs_x, abs_y = rect[0] + x, rect[1] + y

    #領域の始点
    if event == cv2.EVENT_RBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y

    #領域の選択
    if flags == cv2.EVENT_FLAG_RBUTTON:
        img_win = input.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
        cv2.rectangle(img_win, (sx, sy), (x, y), (0, 0, 0), 2)

    #拡大結果の出力
    if event == cv2.EVENT_RBUTTONUP:
        rect_x = np.clip(min(abs_sx, abs_x), 0, input.shape[1] - 2)
        rect_y = np.clip(min(abs_sy, abs_y), 0, input.shape[0] - 2)
        rect_w = np.clip(abs(abs_sx - abs_x), 1, input.shape[1] - rect_x)
        rect_h = np.clip(abs(abs_sy - abs_y), 1, input.shape[0] - rect_y)
        rect = (rect_x, rect_y, rect_w, rect_h)
        img_win = input.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]

    #左クリックしたら移動の始点を決定
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y

    #マウスの動きに合わせて画面移動
    if flags == cv2.EVENT_FLAG_LBUTTON:
        rect_x = np.clip(rect[0] + abs_sx - abs_x, 0, input.shape[1] - rect[2])
        rect_y = np.clip(rect[1] + abs_sy - abs_y, 0, input.shape[0] - rect[3])
        rect_w = rect[2]
        rect_h = rect[3]
        rect = (rect_x, rect_y, rect_w, rect_h)
        img_win = input.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]

#読み込む動画の数は？
while(1):
   print("読み込む動画の数は？(半角数字)")
   file_number = int(input())
   print("%d個" % file_number)
   print("間違いなければokと押してください。")
   k = input()
   if k =="ok":
      break

#動画のディレクトリの確認
while(1):
    print("動画が保存されたディレクトリパスを指定してください。")
    input_path = input()
    print("動画のディレクトリパスは\n %s" % input_path)
    print("指定したディレクトリ内部のリストです。")
    print(os.listdir(input_path))
    print("間違いなければokと入力")
    k = input()
    if k == "ok":
        break

while True:
    print("読み込む動画の形式は？")
    video_format = input()
    print("間違いなければokと入力")
    k = input()
    if k == "ok":
        break

video_frames = []
video_fps = []
video_thumbnail = []



for i in range (int(file_number)):

    input_file = str(i) +"."+ str(video_format)
    print(input_file)
    cap = cv2.VideoCapture(input_file)
    video_frames.append(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    video_fps.append(cap.get(5))
    ret,frame=cap.read()
    video_thumbnail.append(frame)

    #ここでの引数は秒数である。ms出ないことに注意
    time.sleep(0.05)

print(video_thumbnail)
print(video_frames)
print(video_fps)

#一枚目の画像からROIを設定

ROI = []
cv2.namedWindow("thumbnail",cv2.WINDOW_NORMAL)
cv2.setMouseCallback("thumbnail", mouse_callback)
files = int(file_number)

while True:
    for i in range (files):
        print("現在、%d個目の動画のROIを設定しています。")
        thumbnails = str(video_thumbnail[i])
        input = cv2.imread(thumbnails)
        img_win = input.copy()
        while True:
            cv2.imshow("thumbnail", input)
            k = cv2.waitKey(1)

            if k == ord("s"):
                ROI[i] = rect

            # 拡大をリセット
            if k == ord("r"):
                rect = (0, 0, input.shape[1], input.shape[0])
                img_win = input.copy()

            # Escキーを押すと終了
            if k == 27:
                break

     #ROIの要素数が動画の数と一致していたら終了
    if len(ROI) == int(file_number):
        break

#動画をすべてフレーム分割
dir_name = "frame"

if not os.path.exists(dir_name):
   os.mkdir(dir_name)

save_path = os.path.join(input_path, dir_name)

for a in range(files):
    input_file = str(a) + "." + video_format
    cap = cv2.VideoCapture(input_file)
    frames = video_frames[a]

    for i in range(frames):
        ret, frame = cap.read()
        cv2.imwrite("%s/%d_%07d"%(save_path,a,i),frame)

    time.sleep(0.05)

print("フレーム分割完了")

#ROI情報から輝度値を取得する/結果をグラフに出力する。

