
# coding: utf-8

# 「出力データ」
# HSV変換した画像
# HSV変換した画像同士での対応点記述画像
# (計3枚)

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt


# In[7]:


img_path1 = "IMG_4971.JPG"
img_path2 = "IMG_4972.JPG"
img_src1 = cv2.imread(img_path1)
img_src2 = cv2.imread(img_path2)


# HSV変換

# In[8]:


# RGBからHSVに変換
HSVim1 = cv2.cvtColor(img_src1, cv2.COLOR_BGR2HSV)
HSVim2 = cv2.cvtColor(img_src2, cv2.COLOR_BGR2HSV)
# 表示、保存
cv2.imwrite("HSV1.jpg",HSVim1)
cv2.imwrite("HSV2.jpg",HSVim2)


# 特徴量検出

# In[9]:


#AKAZE特徴検出器の作成・初期化 AKAZEをKAZEとしたら、KAZE特徴検出器となる。
akaze = cv2.AKAZE_create()

#特徴量の検出と特徴量ベクトルの計算 kp = keypoint

kp1,des1 = akaze.detectAndCompute(HSVim1,None)
kp2,des2 = akaze.detectAndCompute(HSVim2,None)
print("左　%s" % len(kp1))
print("右　%s" % len(kp2))


# BF、kNNによる対応点探索・評価

# In[10]:


#BF
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k = 2)
print("抜き出される対応点の数　%s" % len(matches))

#kNN
good = [m for m, n in matches if m.distance < .7 * n.distance]
print("間引きされたのちの対応点の数　%s" % len(good))


# 対応点記述

# In[11]:


result = cv2.drawMatchesKnn(HSVim1,kp1,HSVim2,kp2,good,None,flags = 4)

cv2.imwrite("resultcollespondingpoints.jpg",result)

cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.imshow("result",result)

cv2.waitKey()
cv2.destroyAllWindows()

