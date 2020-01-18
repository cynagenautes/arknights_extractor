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

print("ファイルパス等設定(初回)/立ち絵抽出実行 1/2")
a = input()
if a == '1':
    file_list = os.listdir("./Input")
    print("%d件のファイルが見つかりました" %len(file_list))
    print('Start')
    for i in file_list:
        img = cv2.imread("./Input/" + i, cv2.IMREAD_UNCHANGED)
        if img is not None and img.shape[0] > 512:
            if '#' in i:
                if "[alpha]" in i:
                    i2 = i.replace(i[i.find('#'):], '#1[alpha].png')
                    shutil.copy("./Input/" + i, "./Texture2D_B/" + i2)
                    os.remove("./Input/" + i)                   
                else:
                    i2 = i.replace(i[i.find('#'):], '#1.png')
                    shutil.copy("./Input/" + i, "./Texture2D_A/" + i2)
                    os.remove("./Input/" + i)
            else:
                i2 = i.replace(".png", '[alpha].png')
                i3 = i

                shutil.copy("./Input/" + i, "./Texture2D_A/" + i3)
                os.remove("./Input/" + i)
                shutil.copy("./Input/" + i2, "./Texture2D_B/" + i2)
                os.remove("./Input/" + i2)
    print("完了")
    os.system('pause')
if a == '2':
    file_list = os.listdir("./Texture2D_A")
    print("%d件のファイルを処理中" %len(file_list))

    for i in file_list:
        print('%sを処理中' %i)
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
        print("完了 %f s" %(time_end-time_start))
    print('over')
    os.system('pause')