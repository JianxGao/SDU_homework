import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import copy
from scipy.signal import lfilter
from skimage.data import page
from skimage.filters import (threshold_otsu, threshold_niblack,
                             threshold_sauvola)
# 说明：opencv显示图像显示的是BGR，但下面的类操作得到的图像是RGB，可以用cv2.cvtColor(img,cv2.COLOR_BGR2RGB)转一下。


class ImageFunctions(object):
    '''
    Init:
    self.img：输入无论是灰度图还是彩色图，都按彩色图来处理（灰度图堆叠三层）
    self.r：红色分量
    self.g：绿色分量
    self.b：蓝色分量

    Functions:
    show():matplotlib输出图像

    Output:
    输出均为RGB图像，需要opencv处理请务必转BGR

    0. 基础操作:
    brighter():变亮
    dimmer():变暗
    graystyle():灰度图
    binary():黑白图

    1.直方图均衡工具箱
    SSR():SSR去阴影算法，输出彩图而非二值图
    equalization():直方图全局均衡化
    clahe():限制对比度自适应直方图均衡化
    claheYUV():在YUV空间进行clahe
    drag():

    2.核卷积工具箱
    blurry():模糊
    smooth():平滑
    reinforce():模板增强锐化
    USM():USM算法增强锐化
    edgeRef():边缘增强
    edgeRefPlus():边缘增强超级版
    contour():轮廓获取
    edgeGet():边缘检测

    3.二值化工具箱（均针对彩图）
    Otsu():Otsu
    ma():移动平均
    adaptiveThresh():自适应阈值处理
    sauvola():Sauvola最强二值化算法

    4.形态学工具箱
    erode():腐蚀
    dilate():膨胀
    opening():开运算
    closing():闭运算

    5.炫酷滤镜
    memory():复古特效
    yearpass():流年特效

    '''
    def __init__(self, filepath):
        self.img=filepath
        if len(self.img.shape)==3:
            print('3D')
            # 直接把BGR转RGB
            self.r, self.g, self.b = cv2.split(self.img)
            # self.img = cv2.merge([self.r, self.g, self.b])
        elif len(self.img.shape)==2:
            print('2D')
            self.b, self.g, self.r = self.img, self.img, self.img
            self.img=cv2.merge([self.img,self.img,self.img])

    def equalization(self):  # 直方图全局均衡
        r = cv2.equalizeHist(self.r)
        g = cv2.equalizeHist(self.g)
        b = cv2.equalizeHist(self.b)
        img_equalization=cv2.merge([r,g,b])
        #self.show(img_equalization,title='equalization')
        return img_equalization

    def clahe(self):  # 限制对比度自适应直方图均衡化
        clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        r = clahe.apply(self.r)
        g = clahe.apply(self.g)
        b = clahe.apply(self.b)
        img_clahe=cv2.merge([r,g,b])
        #self.show(img_clahe,title='clahe')
        return img_clahe

    def clahe2(self):  # 限制对比度自适应直方图均衡化加强版
        clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(12,12))
        r = clahe.apply(self.r)
        g = clahe.apply(self.g)
        b = clahe.apply(self.b)
        img_clahe=cv2.merge([r,g,b])
        #self.show(img_clahe,title='clahe')
        return img_clahe

    def brighter(self):  # 增亮
        rate=1.1
        img_bright=rate*self.img
        img_bright[img_bright>255]=255
        img_bright=np.round(img_bright)
        img_bright=img_bright.astype(np.uint8)
        #self.show(img_bright,title='brighten')
        return img_bright

    def dimmer(self):  # 变暗
        rate=0.9
        img_dim=self.img*rate
        img_dim=np.round(img_dim)
        img_dim=img_dim.astype(np.uint8)
        #self.show(img_bright,title='brighten')
        return img_dim

    def graystyle(self):  # 灰度图
        # img_gray=0.299*self.r+0.587*self.g+0.114*self.b
        #self.show(img_gray, title='gray')
        img_gray = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)
        img_gray = cv2.merge([img_gray, img_gray, img_gray])
        return img_gray

    def binary(self):  # 黑白图
        img_gray = 0.299 * self.r + 0.587 * self.g + 0.114 * self.b
        img_gray=img_gray.astype(np.uint8)
        blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        ret,img_bi=cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_res=cv2.merge([img_bi,img_bi,img_bi])
        return img_res

    
    def blurry(self):  # 模糊
        kernel=np.array([[1/16,  1/16,  1/16,  1/16,  1/16],
        [1/16,  0,  0,  0,  1/16],
        [1/16,  0,  0,  0,  1/16],
        [1/16,  0,  0,  0,  1/16],
        [1/16,  1/16,  1/16,  1/16,  1/16]],dtype=np.float32)
        dst=cv2.filter2D(self.img,-1,kernel)
        dst=dst.astype(np.uint8)
        #self.show(dst,title='Blurry')
        return dst

    
    def smooth(self):  # 平滑（也就是钝化）
        kernel=np.array([[1/100,  1/100,  1/100,  1/100,  1/100],
        [1/100,  5/100,  5/100,  5/100,  1/100],
        [1/100,  5/100, 44/100,  5/100,  1/100],
        [1/100,  5/100,  5/100,  5/100,  1/100],
        [1/100,  1/100,  1/100,  1/100,  1/100]],dtype=np.float32)
        dst=cv2.filter2D(self.img,-1,kernel)
        dst=dst.astype(np.uint8)
        #self.show(dst,title='Smooth')
        return dst

    
    def reinforce(self):  # 增强并锐化1
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]],dtype=np.float32)
        dst = cv2.filter2D(self.img, -1, kernel)
        dst = dst.astype(np.uint8)
        #elf.show(dst, title='Reinforce')
        return dst

    def USM(self):  # 增强并锐化2
        gauss=cv2.GaussianBlur(self.img, (0, 0), 5)
        usm=cv2.addWeighted(self.img,1.5,gauss,-0.5,0)
        #self.show(usm, title='Reinforce2')
        return usm

    
    def edgeRef(self):  # 边缘增强
        kernel = np.array([[-1/2, -1/2, -1/2],
                           [-1/2, 10/2, -1/2],
                           [-1/2, -1/2, -1/2]], dtype=np.float32)
        dst = cv2.filter2D(self.img, -1, kernel)
        dst = dst.astype(np.uint8)
        #self.show(dst, title='EdgeReinforce')
        return dst

    
    def edgeRefPlus(self):  # 边缘增强超级版
        kernel = np.array([[-1/0.5, -1/0.5, -1/0.5],
                           [-1/0.5, 8.5/0.5, -1/0.5],
                           [-1/0.5, -1/0.5, -1/0.5]], dtype=np.float32)
        dst = cv2.filter2D(self.img, -1, kernel)
        dst = dst.astype(np.uint8)
        #self.show(dst, title='EdgeReinforce_Plus')
        return dst

    
    def contour(self):  # 轮廓
        kernel = np.array([[-1, -1, -1],
                           [-1, 8, -1],
                           [-1, -1, -1]], dtype=np.float32)
        dst = cv2.filter2D(self.img, -1, kernel)
        dst = dst.astype(np.uint8)
        #self.show(dst, title='contour')
        return dst

    
    def edgeGet(self):  # 边界提取
        gauss = cv2.GaussianBlur(self.img, (5, 5), 0)
        img_bi = cv2.Canny(gauss, 50, 230)
        #self.show(img_bi, title='edgeGet')
        return img_bi

    def Otsu(self):  # Otsu
        blur = cv2.GaussianBlur(self.r, (5, 5), 0)
        ret,img_bir=cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(self.g, (5, 5), 0)
        ret, img_big = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(self.b, (5, 5), 0)
        ret, img_bib = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_bi=cv2.merge([img_bir,img_big,img_bib])
        # self.show(img_bi,title='Otsu')
        return img_bi

    def memory(self):  # 复古模式
        r=0.393*self.r+0.769*self.g+0.189*self.b
        g=0.349*self.r+0.686*self.g+0.168*self.b
        b=0.272*self.r+0.534*self.g+0.131*self.b
        rth=np.where(r>255)
        if len(rth[0])>0:
            for i in range(len(rth[0])):
                r[rth[0][i]][rth[1][i]]=255
        gth = np.where(g > 255)
        if len(gth[0]) > 0:
            for i in range(len(gth[0])):
                g[gth[0][i]][gth[1][i]]=255
        bth = np.where(b > 255)
        if len(bth[0])>0:
            for i in range(len(bth[0])):
                b[bth[0][i]][bth[1][i]] = 255
        dst=cv2.merge([r,g,b])
        dst=dst.astype(np.uint8)
        #self.show(dst,title='memory')
        return dst

    def yearpass(self):  # 流年特效
        # r=1*self.r
        # g=1*self.g
        # b=12*np.sqrt(self.b)
        # bth = np.where(b > 255)
        # if len(bth[0])>0:
        #     for i in range(len(bth[0])):
        #         b[bth[0][i]][bth[1][i]] = 255
        # b=b.astype(np.uint8)
        # dst = cv2.merge([r, g, b])
        # dst = dst.astype(np.uint8)
        # return dst
        b=1*self.b
        g=1*self.g
        r=12*np.sqrt(self.r)
        rth = np.where(r > 255)
        if len(rth[0])>0:
            for i in range(len(rth[0])):
                r[rth[0][i]][rth[1][i]] = 255
        r=r.astype(np.uint8)
        dst = cv2.merge([r, g, b])
        dst = dst.astype(np.uint8)
        return dst

    
    def erode(self):  # 腐蚀
        ero=cv2.erode(self.img, kernel=np.ones((5, 5), np.uint8))
        #self.show(ero, title='erode')
        return ero

    
    def dilate(self):  # 膨胀
        dilation = cv2.dilate(self.img, kernel=np.ones((5, 5),np.uint8), iterations=1)
        #self.show(dilation, title='dilate')
        return dilation

    
    def opening(self):  # 开运算
        opening = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel=np.ones((5, 5),np.uint8))
        #self.show(opening, title='open')
        return opening

    
    def closing(self):  # 开运算
        closing = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel=np.ones((5, 5),np.uint8))
        #self.show(closing, title='close')
        return closing

    
    def ma(self,n=10,k=0.5): # 移动平均
        shape=self.img.shape
        f1=self.img.copy()
        assert n>=1
        assert 0<k<1
        f1[1:-1:2, :] = np.fliplr(self.img[1:-1:2, :])
        f1 = f1.flatten()
        maf = np.ones(n) / n
        res_filter = lfilter(maf, 1, f1)
        g = np.array(f1 > k * res_filter).astype(int)
        g = g.reshape(shape)
        g[1:-1:2, :] = np.fliplr(g[1:-1:2, :])
        print(g)
        g = g * 255
        # self.show(g,title='moving average')
        return g

    def adaptiveThresh(self, winSize=11, ratio=0.15):  # winSize越小越模糊，ratio越大越模糊
        mean = cv2.boxFilter(self.img, cv2.CV_32FC1, (winSize, winSize))  # 均值平滑
        out = self.img - (1.0 - ratio) * mean  # 原图像与平滑结果做差
        out[out >= 0] = 255
        out[out < 0] = 0
        out = out.astype(np.uint8)
        # self.show(out,title='adaptiveThresh')
        return out

    def sauvola(self, windowSize=15, k=0.2):  # Sauvola最强二值化算法
        imgcpy = copy.deepcopy(self.img)
        threshold = threshold_sauvola(imgcpy, windowSize, k)
        print(threshold)
        imgcpy[imgcpy > threshold] = 255
        imgcpy[imgcpy < threshold] = 0
        return imgcpy

    def auxDrag(self,l, x1, y1, x2, y2):
        l = l.astype(np.float32)
        l[l < x1] = l[l < x1] * (y1 / x1)
        l[(l >= x1) & (l <= x2)] = (y2 - y1) / (x2 - x1) * (l[(l >= x1) & (l <= x2)] - x1) + y1
        l[l > x2] = (255 - y2) / (255 - y1) * (l[l > x2] - x2) + y2
        l = l.astype(np.uint8)
        return l

    def drag(self, x1=100, y1=50, x2=155, y2=200):
        b, g, r = cv2.split(self.img)
        b_new = self.auxDrag(b, x1, y1, x2, y2)
        g_new = self.auxDrag(g, x1, y1, x2, y2)
        r_new = self.auxDrag(r, x1, y1, x2, y2)
        im_final = cv2.merge([b_new, g_new, r_new])
        im_final = im_final.astype(np.uint8)
        return im_final

    def claheYUV(self):
        imgYUV = cv2.cvtColor(self.img, cv2.COLOR_RGB2YCrCb)
        channelsYUV = cv2.split(imgYUV)
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
        channelsYUV[0] = clahe.apply(channelsYUV[0])
        channels = cv2.merge(channelsYUV)
        result = cv2.cvtColor(channels, cv2.COLOR_YCrCb2RGB)
        return result

    
    def SSR(self, sigma=111):
        _temp = cv2.GaussianBlur(self.img, (0, 0), sigma)
        gaussian = np.where(_temp == 0, 0.01, _temp)
        img_ssr = np.log10(self.img + 0.01) - np.log10(gaussian)
        for i in range(img_ssr.shape[2]):
            img_ssr[:, :, i] = (img_ssr[:, :, i] - np.min(img_ssr[:, :, i])) / \
                               (np.max(img_ssr[:, :, i]) - np.min(img_ssr[:, :, i])) * 255
        img_ssr = np.minimum(np.maximum(img_ssr, 0), 255).astype(np.uint8)
        # img_ssr = cv2.cvtColor(img_ssr, cv2.COLOR_BGR2RGB)
        return img_ssr


if __name__ == '__main__':
    X=ImageFunctions('lrz2.png')