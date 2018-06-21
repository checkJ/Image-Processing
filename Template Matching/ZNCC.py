#-*- coding:utf-8 -*-
import cv2
import numpy as np

def main():
    # 入力画像とテンプレート画像をで取得
    img = cv2.imread("erena.jpg")
    temp = cv2.imread("erena temp.jpg")

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)

    # テンプレート画像の高さ・幅
    h, w = temp.shape

    # テンプレートマッチング（OpenCVで実装）
    #cv2.TM_CCOEFF_NORMEDがZNCCを表している
    match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)

    #検出結果から検出領域の位置情報を取得する
    min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
    pt = max_pt

    #検出された箇所の左上の画素値
    print(pt)
    print(type(pt))

    #検出された箇所の中央画素値
    pt_Center = (round(pt[0]+w/2), round(pt[1]+h/2))
    print(pt_Center)

    # テンプレートマッチングの結果を出力
    cv2.rectangle(img, (pt[0], pt[1] ), (pt[0] + w, pt[1] + h), (0,0,200), 3)
    cv2.imwrite("output.png", img)


if __name__ == "__main__":
    main()