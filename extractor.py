# -*- coding: utf-8 -*- 
import shutil
import time
import cv2
import os

def read_png(s):
    img = cv2.imread(s, cv2.IMREAD_UNCHANGED) 
    return img

def save_png(s, img):
    cv2.imwrite(s, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

def exchange(img, x):
    w, h = img.shape[0:2]
    tempimg = cv2.resize(img,(w*x,h*x), interpolation=cv2.INTER_CUBIC)
    return tempimg

def Do(a, b):
    a[:,:,3] = b[:,:,0]
    return a

print("提取图片/合成立绘？1/2")
a = input()
if a == '1':
    file_list = os.listdir("./Input")
    print("共%d个图片：" %len(file_list))
    print('begin')
    for i in file_list:
        img = cv2.imread("./Input/" + i, cv2.IMREAD_UNCHANGED)
        if img is not None and img.shape[0] > 512:
            if '#' in i:
                i2 = i.replace(i[i.find('#'):], '#1[alpha].png')
                i3 = i.replace(i[i.find('#'):], '#1.png')
            else:
                i2 = i.replace(".png", '[alpha].png')
                i3 = i
            if i2 in file_list:
                shutil.copy("./Input/" + i, "./Texture2D_A/" + i3)
                os.remove("./Input/" + i)
                shutil.copy("./Input/" + i2, "./Texture2D_B/" + i2)
                os.remove("./Input/" + i2)
    print('over')
    os.system('pause')
if a == '2':
    file_list = os.listdir("./Texture2D_A")
    print("待合成%d个图片：" %len(file_list))

    for i in file_list:
        print('正在处理%s' %i)
        time_start = time.time()
        i2 = i.replace(".png", '[Alpha].png')
        a = read_png('./Texture2D_A/' + i)
        b = read_png('./Texture2D_B/' + i2)
        if a.shape[0]/b.shape[0] != 1:
            b = exchange(b, int(a.shape[0]/b.shape[0]))
        save_png('./Picture/' + i, Do(a, b))
        shutil.copy("./Texture2D_A/" + i, "./Used/" + i)
        os.remove("./Texture2D_A/" + i)
        time_end = time.time()
        print("耗时 %f s" %(time_end-time_start))
    print('over')
    os.system('pause')