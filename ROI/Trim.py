import cv2
import os



#ROIの起点
ROI_s =[710, 620]
#ROIの終点
ROI_e = [810, 740]

file_path = "F:\\Deep Learning\\0625\\images"
os.chdir(file_path)

cd = os.getcwd()
print(cd)
dir_name = "templates"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)



for i in range (50):
    img_name = str(i)+".bmp"
    print(img_name)
    input_img = cv2.imread(img_name)
    trim = input_img[620:740, 710:810]
    save_name1 = "trim%2d.bmp" %i
    cv2.imwrite(dir_name+"\\"+save_name1,trim)

os.chdir(cd)

dir_name = "Blur_templates"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)


for i in range (50):
    input_img = cv2.imread(str(i) + ".bmp")
    blur = cv2.blur(input_img, (10, 10))

    trim_blur = blur[620:740, 710:810]
    save_name2 = "Blur_trim%2d.bmp" % i

    cv2.imwrite(dir_name + "\\"+save_name2, trim_blur)

