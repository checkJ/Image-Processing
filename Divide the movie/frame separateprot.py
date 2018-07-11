#-*- coding:utf-8 -*-

import cv2
import sys
import re
import os
import time
import tkinter
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog

#Directory pathをGUIで指定できるようにする
#引数は最初に表示するdirectory　path
def fileopenGUI(init_dir):
    root=tkinter.Tk()
    root.withdraw()
    initialdirectory = init_dir
    fname = tkFileDialog.askdirectory(initialdir= initialdirectory )
    #tkMessageBox.showinfo('Dirctory Path ',fname)
    root.withdraw()
    return fname


#指定シタディレクトリの中に、欲しい拡張子のファイルを# 確認する
#さらに、名前をリストに入れて返す
#引数は検索対象のdirectory　path, 確認したい拡張子
def count_file(path, extension):
    namelist = []
    for file in os.listdir(path):
        base,ext = os.path.splitext(file)
        if ext == extension:
            namelist.append(file)
    return namelist




#入力ファイルパス決定・動画の数の確認
while True:
    # 処理したい動画が入っているdirectoryを指定
    cd = os.path.abspath(os.getcwd())
    input_path = fileopenGUI(cd)
    print(input_path)
    # 指定したディレクトリの中にある動画の数を確認
    # 合っているか確認を取り、間違っていればpath指定からやり直す
    movie_list = count_file(input_path, ".MP4")
    if len(movie_list) == 0:
        print("動画ファイルが見つかりませんでした。")
        continue

    else:
        print("動画ファイルが%d個見つかりました。"
              "処理を続行しますか？" % len(movie_list))
        a = input("[y/n]")

        if a == "y":
            break
        else:
            print("やり直し")
            continue

#保存先のディレクトリの設定
while True:
    save_path = fileopenGUI(input_path)
    print("save_path : %s"%str(save_path))
    c = input("OK?[y/n]")
    if c == "y":
        break
    else:
        continue

start = time.time()


for a in range(len(movie_list)):
    # 読み込む動画の長さとfpsの設定値を入力
    file_name = movie_list[a]
    file_path = input_path
    os.chdir(input_path)

    # 動画の読み込み。ここで指定したインスタンスが以降の動画操作系のコマンドに継承されていく
    file_name = os.path.join(file_path, file_name)
    cap = cv2.VideoCapture(file_name)

    os.chdir(save_path)
    # スクリーンキャプチャを保存するdirectory設定
    dir_name = str(movie_list[a])

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    os.chdir(dir_name)


    # 動画のフレーム数を確認。のちのforループで使用するのでint型に指定
    frame_count = int(cap.get(7))

    # フレームを連番画像として保存
    for i in range(frame_count):

        ret, frame = cap.read()
        cv2.imwrite("%05d.png" % i, frame)
        percent = int(i/frame_count)
        sys.stdout.write("\r %d / %d個目 %d %% completed!"%(a,len(movie_list), percent))


#動画の長さと処理時間の関係
end = time.time() - start



print("%s 秒かかりました"%end)
