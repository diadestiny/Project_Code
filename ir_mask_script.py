import xml.etree.ElementTree as ET
import sys
import os
import cv2
import datetime as dt
import random
import numpy as np


class splitImg():
    def __init__(self, savePath, xmlsPath, imgpath):
        self.xmin = []
        self.ymax = []
        self.ymin = []
        self.xmax = []

        self.imgpath = imgpath
        self.name = []

        self.savePath = savePath
        self.xmlsPath = xmlsPath

    def read_xml(self, filename):
        xywh = []
        self.name = []
        self.ymin = []
        self.xmin = []
        self.ymax = []
        self.xmax = []
        # 读取xml文件获取信息
        # print(filename)
        tree = ET.parse(filename)
        # self.imgPath = tree.findall("annotation")[0].text
        for i in range(len(tree.findall("object"))):
            x1 = tree.findall("object")[i].find("bndbox")[0].text
            y1 = tree.findall("object")[i].find("bndbox")[1].text
            x2 = tree.findall("object")[i].find("bndbox")[2].text
            y2 = tree.findall("object")[i].find("bndbox")[3].text
            # self.xmin.append(tree.findall("object")[i].find("bndbox")[0].text)
            # self.ymin.append(tree.findall("object")[i].find("bndbox")[1].text)
            # self.xmax.append(tree.findall("object")[i].find("bndbox")[2].text)
            # self.ymax.append(tree.findall("object")[i].find("bndbox")[3].text)
            # self.name.append(tree.findall("object")[i].find("name").text)
            xywh.append([int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1)])
        return xywh

    def mosaic_effect(self, xywh, imgPath):
        img = cv2.imread(imgPath)
        height, width, n = img.shape
        new_img = img.copy()
        # size = 1
        # hard:(1,3)
        # mid:(3,5)
        # easy:(5,7)
        for [x, y, w, h] in xywh:
            step_i = random.randint(5, 7)
            for i in range(y, (y + h), step_i):
                step_len = random.randint(5, 7)
                for j in range(x, (x + w), step_len):
                    # if i - size > 0 and j + size < width and i + size < height and j - size > 0:
                    # i_rand = random.randint(i - size, i)
                    # j_rand = random.randint(j - size, j)
                    # new_img[i,j] =  img[i_rand, j_rand, :]
                    new_img[i, j] = [255, 255, 255]
        return new_img
        # print(len(tree.findall("object")))
        # print(self.imgPath, "\n", self.box, "\n", self.name, "\n")

    def irregular_mask(self, xywh, imgPath,max_angle=5, max_len=8, max_width=5, times=4):
        # hard:max_angle=10, max_len=15, max_width=10, times=8
        # mid:max_angle=5, max_len=8, max_width=5, times=4
        # easy:max_angle=3, max_len=4, max_width=2, times=3
        print(imgPath)
        img = cv2.imread(imgPath)
        height, width, n = img.shape
        new_img = img.copy()
        mask = np.zeros((height, width), np.float32)
        # mask = np.zeros((max_size, max_size), np.float32)
        # times = np.random.randint(8)
        for [x, y, w, h] in xywh:
            for i in range(times):
                # start_x = np.random.randint(x,x+w)
                # start_y = np.random.randint(y,y+h)
                # print(x,x+w,y,y+h)
                # print(start_x,start_y)
                start_x,start_y = int(x+w/2.5),int(y+h/2)
                for j in range(0,5):
                    angle = 0.01 + np.random.randint(max_angle)
                    if i % 2 == 0:
                        angle = 2 * 3.1415926 - angle
                    # length = 5 + np.random.randint(5, max_len)
                    # brush_w = 3 + np.random.randint(1, max_width)
                    end_x = (start_x + max_len * np.sin(angle)).astype(np.int32)
                    end_y = (start_y + max_len * np.cos(angle)).astype(np.int32)
                    # print(x+(w/0.75),x,w)
                    if end_x>x+w*0.85 or end_x<x+w*0.15 or end_y<y+h*0.15 or end_y>y+h*0.85:
                        j = j - 1
                        j = max(0, j)
                    else:
                        cv2.line(mask, (start_x, start_y), (end_x, end_y), 1.0, max_width)
                        start_x, start_y = end_x, end_y

        new_img[mask==1] = [255, 255, 255]
        return new_img

    def selectROI(self):
        # 截取roi区域
        img = cv2.imread(self.imgPath)
        # print(self.ymin, "\n", self.ymax, "\n", self.xmin, self.xmax, "\n")
        for i in range(len(self.name)):
            roiImg = img[int(self.ymin[i]):int(self.ymax[i]), int(self.xmin[i]):int(self.xmax[i])]
            # 根据系统时间命名图像
            now_time = dt.datetime.now().strftime("%Y%m%d%H%M%S%f")
            saveName = os.path.join(self.savePath + "/" + self.name[i] + "/", str(now_time)[6:] + ".jpg")
            if not os.path.exists(self.savePath + "/" + self.name[i] + "/"):
                os.mkdir(self.savePath + "/" + self.name[i] + "/")
            cv2.imwrite(saveName, roiImg)
            cv2.waitKey(1)

    def run(self):
        for file in os.listdir(self.xmlsPath):
            if file.split(".")[1] == "xml":
                path = os.path.join(self.xmlsPath, file)
                xywh = self.read_xml(path)
                img_path = os.path.join(self.imgpath, file.replace('xml', 'jpg'))
                new_img = self.irregular_mask(xywh, img_path)
                save_path = os.path.join(self.savePath, file.replace('xml', 'jpg'))
                cv2.imwrite(save_path, new_img)
                print(save_path)
                # break
                # self.selectROI()


if __name__ == '__main__':
    xmlPath = "E:/项目数据集/孪生网络/warship/annotations/"  # xml存储的根目录路径
    imgPath = "images/"
    savePath = "./ir_mid/"  # 需要保存截取图像的位置
    aa = splitImg(savePath, xmlPath, imgPath)
    aa.run()
