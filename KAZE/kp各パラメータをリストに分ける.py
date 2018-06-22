
# coding: utf-8

# In[100]:


import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import collections


# In[101]:


img_path = "IMG_4956.JPG"
img = cv2.imread(img_path)


# In[102]:


akaze = cv2.AKAZE_create()

kp,des = akaze.detectAndCompute(img,None)


# In[103]:


f4 = cv2.drawKeypoints(img,kp,cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG,color=(255.0,255),flags=4)
cv2.namedWindow("flag 4",cv2.WINDOW_NORMAL)
cv2.imshow("flag 4",f4)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("result4.jpg",f4)


# In[78]:


m = len(kp)
print(m)
#特徴点強度のリストを作成
response = [kp[n].response for n in range(1,m)]
plt.plot(response)


# In[80]:


#python3から、xrangeではなくrangeで
size = [kp[n].size for n in range(1,len(kp))]
plt.plot(size)


# In[7]:


kp[3].size


# In[8]:


kp[100].size

