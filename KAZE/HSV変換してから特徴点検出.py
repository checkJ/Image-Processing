
# coding: utf-8

# 「出力」
# HSV変換画像
# オリジナルとHSVの特徴点記述画像
# (計3枚)

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


# In[2]:


t1 = time.time()


# In[ ]:


img_path = "IMG_4967.JPG"
img_src = cv2.imread(img_path)


# HSV変換

# In[ ]:


# RGBからHSVに変換
HSVim = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)

# 表示、保存
#cv2.namedWindow("HSV convert",cv2.WINDOW_NORMAL)
#$cv2.imshow("HSV convert", HSVim)
cv2.imwrite("HSV.jpg",HSVim)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imwrite("HSVconvert.jpg",HSVim)


# オリジナルとHSV画像の特徴量検出

# In[ ]:


#AKAZE特徴検出器の作成・初期化 AKAZEをKAZEとしたら、KAZE特徴検出器となる。
akaze = cv2.AKAZE_create()

#特徴量の検出と特徴量ベクトルの計算 kp = keypoint

kp1,des1 = akaze.detectAndCompute(img_src,None)
kp2,des2 = akaze.detectAndCompute(HSVim,None)
print("オリジナル　%s" % len(kp1))
print("HSV　%s" % len(kp2))


# 特徴点記述

# In[ ]:


kpshow = cv2.drawKeypoints(img_src,kp1,cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG,color=(255.0,255),flags=4)
HSVkpshow = cv2.drawKeypoints(HSVim,kp2,cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG,color=(255.0,255),flags=4)

#cv2.namedWindow("Origin",cv2.WINDOW_NORMAL)
#cv2.imshow("Origin",kpshow)
cv2.imwrite("Horiginal kp.jpg",kpshow)
#cv2.namedWindow("HSVkp",cv2.WINDOW_NORMAL)
#cv2.imshow("HSVkp",HSVkpshow)
cv2.imwrite("HSVkp.jpg",HSVkpshow)

#cv2.waitKey(0)
#cv2.destroyAllWindows()


# In[ ]:


t2 = time.time()
t3 = t2- t1
print(t3)

