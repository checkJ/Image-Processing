# coding utf-8

import os
import cv2
import sys
import csv
import random
import shutil


# モード選択
modeD = False
modeC = False
modeE = False

# データセット作成時の変数
o_path = 'data\original\\'
t_path = 'data\\tr_img\\'
l_path = 'data\lr_img\\'
files0 = []
files1 = []
texts0 = []
texts1 = []
num = 0
n = 0

# CSV作成時の変数
l_add  = 'lr_img/'
t_add  = 'tr_img/'
train  = 'data\imgUp_train.csv'
test   = 'data\imgUp_test.csv'
execu  = 'data\imgUp_execu.csv'
rate   = 70

# Executor作成時の変数
in_path = 'data\executor\input\\'
ou_path = 'data\executor\output\\'
fa_path = 'data\executor\\fake\\'
in_add  = 'executor/input/'
fa_add  = 'executor/fake/'
sam_add = 'data\executor\sample.jpg'

# MODE確認
sys.stdout.write("データセットを作成しますか？(y/n)⇒ ")
mode = input()
if mode == 'y':
    modeD = True
elif mode == 'n':
    modeD == False
else:
    sys.stdout.write("不適切な文字が与えられました\n")
    sys.exit()
sys.stdout.write("CSVを作成しますか？(y/n)⇒ ")
mode = input()
if mode == 'y':
    modeC = True
elif mode == 'n':
    modeC == False
else:
    sys.stdout.write("不適切な文字が与えられました\n")
    sys.exit()
sys.stdout.write("Executorデータを作成しますか？(y/n)⇒ ")
mode = input()
if mode == 'y':
    modeE = True
elif mode == 'n':
    modeE == False
else:
    sys.stdout.write("不適切な文字が与えられました\n")
    sys.exit()


for x in os.listdir(o_path):
    if os.path.isfile(o_path + x):
        files0.append(x)
for y in files0:
    if(y[-4:] == '.jpg'):
        texts0.append(y)


sys.stdout.write("Seting up project folder\n")
if modeD:
    if os.path.exists(t_path):
        shutil.rmtree(t_path)
        sys.stdout.write("Removed tr_img\n")
    if os.path.exists(l_path):
        shutil.rmtree(l_path)
        sys.stdout.write("Removed lr_img\n")
if modeE:
    if os.path.exists(in_path):
        shutil.rmtree(in_path)
        sys.stdout.write("Removed input\n")
    if os.path.exists(ou_path):
        shutil.rmtree(ou_path)
        sys.stdout.write("Removed output\n")
    if os.path.exists(fa_path):
        shutil.rmtree(fa_path)
        sys.stdout.write("Removed fake\n")
if modeD:
    os.mkdir(t_path)
    os.mkdir(l_path)
if modeE:
    os.mkdir(in_path)
    os.mkdir(ou_path)
    os.mkdir(fa_path)
sys.stdout.write("Setup complete\n\n")


if modeD:
    sys.stdout.write("Creating Dataset\n")
    for x in texts0:
        img = cv2.imread(o_path+x, cv2.IMREAD_UNCHANGED)

        if img is None:
            sys.stdout.write("Failed to load image file.\n")
            sys.exit(1)

        if len(img.shape) == 3:
            height, width, channels = img.shape[:3]
        else:
            height, width = img.shape[:2]
            channels = 1

        numX = width // 33
        numY = height // 33

        for i in range(numX):
            for j in range(numY):
                cropped_img = img[33*j:33*(j+1),33*i:33*(i+1)]
                small_img = cv2.resize(cropped_img,(11,11))
                tr_img = cropped_img[6:27,6:27]
                lr_img = cv2.resize(small_img,(33,33))

                cv2.imwrite(t_path + ('%06d'%num) + ".jpg",tr_img)
                cv2.imwrite(l_path + ('%06d'%num) + ".jpg",lr_img)
                num = num + 1

        n = n + 1
        sys.stdout.write("\r" + str(n) + "/" + str(len(texts0)))
    num = 0
    n = 0
    sys.stdout.write("\nDataset Created!\n\n")


if modeC:
    sys.stdout.write("Creating CSV\n")
    for x in os.listdir(l_path):
        if os.path.isfile(l_path + x):
            files1.append(x)
    for y in files1:
        if(y[-4:] == '.jpg'):
            texts1.append(y)

    full = len(texts1)
    rate = (full*rate)//100
    li = list(range(full))
    random.shuffle(li)

    with open(train, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator="\n")
        writer.writerow(["x:image","y:image"])
        for i in range(rate):
            writer.writerow([l_add+'%06d'%li[i]+".jpg",t_add+'%06d'%li[i]+".jpg"])

    with open(test, "w") as csvfile:
        writer = csv.writer(csvfile,delimiter=',',lineterminator="\n")
        writer.writerow(["x:image","y:image"])
        for i in range(full - rate):
            writer.writerow([l_add+'%06d'%li[i+rate]+".jpg",t_add+'%06d'%li[i+rate]+".jpg"])
    num = 0
    n = 0
    sys.stdout.write("CSV Created!\n\n")


if modeE:
    sys.stdout.write("Creating Executor\n")
    img = cv2.imread(sam_add, cv2.IMREAD_UNCHANGED)

    if img is None:
        sys.stdout.write("Failed to load image file.\n")
        sys.exit(1)
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1

    big_img = cv2.resize(img,(width*3,height*3))
    numX = (width*3-12) // 21
    numY = (height*3-12) // 21
    sum_num = numX*numY

    src_img = big_img[0:numY*21+12,0:numX*21+12]

    for i in range(numX):
        for j in range(numY):
            input_img = src_img[21*j:21*j+33,21*i:21*i+33]
            fake_img = input_img[6:27,6:27]

            cv2.imwrite(in_path + ('%06d'%num) + ".jpg",input_img)
            cv2.imwrite(fa_path + ('%06d'%num) + ".jpg",fake_img)
            num = num + 1

            sys.stdout.write("\r" + str(num) + "/" + str(sum_num))


    with open(execu, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator="\n")
        writer.writerow(["x:image","y:image"])
        for i in range(sum_num):
            writer.writerow([in_add+'%06d'%i+".jpg",fa_add+'%06d'%i+".jpg"])


    sys.stdout.write("\nExecutor Created!\n\n")
sys.stdout.write("\nCompleted!!")