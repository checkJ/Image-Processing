import cv2
import numpy as np


#画像読み込み
print("読み込む画像の名前を入れてください")
input_img = "sample.png"

input = cv2.imread(input_img)
img_win =input.copy()



#原点、原点、横幅、高さ
rect = (0, 0, input.shape[1], input.shape[0])

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


cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("img", mouse_callback)
ROI = []

while(1):
    cv2.imshow("img", img_win)
    k = cv2.waitKey(1)
    print(rect)

    #Sキーを押したらROIの範囲を変数ROIに格納
    if k == ord("s"):
        roi = input[rect[0]:rect[0]+rect[2], rect[1]:rect[1]+rect[3]]
        ROI = rect


    #Escキーを押すと終了
    if k == 27:
        break

    #拡大をリセット
    if k == ord("r"):
        rect = (0, 0, input.shape[1], input.shape[0])
        img_win = input.copy()

print("結果")
print(ROI)