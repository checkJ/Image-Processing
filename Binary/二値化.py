
# coding: utf-8

# In[49]:


# -*- coding: utf-8 -*-
 
import cv2
import numpy as np
import os
 
if __name__ == '__main__':
 
    # 画像の読み込み
    #入力画像の名前
    input_name = "24.jpg"
    cd = os.getcwd()
    input_dir = "/input/"
    img_src = cv2.imread(cd + input_dir+ input_name)
 
    # グレースケールに変換
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
 
    # 二値変換
    thresh = 60
    max_pixel = 255
    ret, img_dst = cv2.threshold(img_gray,
                                 thresh,
                                 max_pixel,
                                 cv2.THRESH_BINARY_INV)
 
    # 表示
    cv2.namedWindow("Result Image",cv2.WINDOW_NORMAL)
    cv2.imshow("Result Image", img_dst)
    cv2.imwrite("Binary_24.jpg",img_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 閾値の設定はどうする？

# 低特徴が前提であるので輝度値の最頻値を求めて閾値として設定すればいいと思う
