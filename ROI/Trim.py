import cv2
import os



#ROIの起点
ROI_s =[710, 620]

#ROIの終点
ROI_e = [810, 740]

#トリミングしたい画像が入っているdirectorypath
input_path = "F:\\Deep Learning\\0625\\images"


os.chdir(input_path)
cd = os.getcwd()

#保存するdirectory name
dir_name = "templates"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

#directory内部の画像枚数を調べる
number_images = []
number_images =os.listdir(input_path)


for i in range (len(number_images)):
    img_name = str(i)+".bmp"
    print(img_name)
    input_img = cv2.imread(img_name)
    trim = input_img[620:740, 710:810]
    save_name1 = "trim%d.bmp" %i
    cv2.imwrite(dir_name+"\\"+save_name1,trim)

os.chdir(cd)


