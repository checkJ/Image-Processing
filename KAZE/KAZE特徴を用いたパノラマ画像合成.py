
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import numpy.linalg as LA
import os
import winsound
import time


# In[2]:


t1 = time.time()


# 画像読み込み

# In[3]:


img1_path = "IMG_4989.JPG"
img2_path = "IMG_4990.JPG"
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)


# KAZE特徴検出器

# In[4]:


detector = cv2.AKAZE_create()
kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)
print(len(kp1))
print(len(kp2))


# BFマッチング

# In[5]:


bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.match(des1, des2)


# トレーニングおよびクエリ特徴量のインデックスをリスト化

# In[6]:


dist = [m.distance for m in matches]
thres_dist = (sum(dist) / len(dist)) * 0.9
sel_matches = [m for m in matches if m.distance < thres_dist]
point1 = [[kp1[m.queryIdx].pt[0], kp1[m.queryIdx].pt[1]] for m in sel_matches]
point2 = [[kp2[m.trainIdx].pt[0], kp2[m.trainIdx].pt[1]] for m in sel_matches]
point1 = np.array(point1)
point2 = np.array(point2)


# ホモグラフィ変換

# In[7]:



H, Hstatus = cv2.findHomography(point1,point2,cv2.RANSAC)


def conv_uv(u, v, H): 
    ud, vd, nm = np.dot(H, np.array([u, v, 1]))
    ud, vd = ud/nm, vd/nm
    return ud, vd

def calc_w(u, v, w, h):
    return min([v, u, h-v, w-u])

def calc_w_h(w, h, H):
 
    lt_u, lt_v = conv_uv(0, 0, H)
    rt_u, rt_v = conv_uv(w, 0, H)
    lb_u, lb_v = conv_uv(0, h, H)
    rb_u, rb_v = conv_uv(w, h, H)

    min_v = min([lt_v, rt_v, 0])
    max_v = max([lb_v, rb_v, h])
    min_u = min([lt_u, rt_u, 0])
    max_u = max([lb_u, rb_u, w])

    is_w = int(round(max_u - min_u))
    is_h = int(round(max_v - min_v))
    return is_w, is_h, -int(min_v)

i1_h, i1_w = img1.shape[0], img1.shape[1]
i2_h, i2_w = img2.shape[0], img2.shape[1]

H = np.array(H)
iH = LA.inv(H)

is_w, is_h, offset = calc_w_h(i2_w, i2_h, iH)

simg = np.zeros((is_h, is_w, 3), np.uint8)


for v1 in range(i1_h):
    for u1 in range(i1_w):
        simg[v1+offset, u1] = img1[v1, u1]


for v1 in range(-offset, is_h-offset):
    for u1 in range(is_w):
        i2_p = 0
        u2, v2 = conv_uv(u1, v1, H)
        
        if (u2 > 0 and u2 < i2_w) and (v2 > 0 and v2 < i2_h):
            u2_, v2_ = float(int(u2)), float(int(v2))
            wu, wv = u2 - u2_, v2 - v2_
            p1 = img2[int(v2_), int(u2_)]
            if int(u2_) > i2_w-2 or int(v2_) > i2_h-2:
              
                i2_p = p1
            else:
          
                p2 = img2[int(v2_), int(u2_)+1]
                p3 = img2[int(v2_)+1, int(u2_)]
                p4 = img2[int(v2_)+1, int(u2_)+1]
                i2_p = (1-wu)*(1-wv)*p1+wu*(1-wv)*p2+(1-wu)*wv*p3+wu*wv*p4
        
            if simg[v1+offset, u1].all(): # if overlap
                w1, w2 = float(calc_w(v1+offset, u1, i1_w, i1_h)), float(calc_w(v2, u2, i2_w, i2_h))
                if (w1 == 0 and w2 == 0) or w1*w2 < 0: 
                    pass
                else:
                    wt1, wt2 = w1/(w1+w2), w2/(w1+w2)
                    p = wt1*simg[v1+offset, u1] + wt2*i2_p 
                    simg[v1+offset, u1] = p
            else:
                simg[v1+offset, u1] = i2_p
                


# In[8]:


cv2.imwrite("stitch_image.jpg", simg)


cv2.imshow("image", simg)
t2 = time.time()
t3 = t2- t1
print(t3)
winsound.Beep(523,200)
cv2.waitKey(0)

