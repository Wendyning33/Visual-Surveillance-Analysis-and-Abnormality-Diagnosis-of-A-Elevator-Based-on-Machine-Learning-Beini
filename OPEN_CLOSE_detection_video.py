# 输入图片，取上半部分[5:200,580:970]，反色（黑白互换），提高对比度和亮度，最终图像：processed_lift
# 当num_black>100时，门打开状态； 当num_black<=100时，门关闭状态。阈值取自于10人视频的第65帧。
import cv2 as cv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from scipy import ndimage
from PIL import Image
from pylab import *

def inverse_image_demo(image):
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    height = gray.shape[0]
    width = gray.shape[1]
    for row in range(height):
        for col in range(width):
            pv = gray[row, col]
            gray[row, col] = 255 - pv
    return gray

def contrast_brightness_demo(image,c,b):
    #c是对比度，1.2，1.5，其实是每一个像素乘以c；
    #b是亮度，比如20是提高一般亮度，100会容易曝光，其实就是每一个像素加上b
    h,w = image.shape
    blank = np.zeros([h,w],image.dtype)
    dst = cv.addWeighted(image,c,blank,1-c,b)
    return dst

def threshold_demo(image):
    ret,binary = cv.threshold(image,0,255,cv.THRESH_BINARY | cv.THRESH_TRIANGLE)#cv.THRESH_OTSU
    #上一行最后，这里的cv.THRESH_TRIANGLE也可以换成cv.THRESH_OTSU
    #print("threshold value:%s"%ret)
    #cv.imwrite("binary_demo.png",binary)
    return binary

#仅垂直的直线检测
def open_demo(image):#开操作
    cv.imshow("ori_edges",image)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(1,15))
    open_demo = cv.morphologyEx(image,cv.MORPH_OPEN,kernel)
    cv.imshow("open_demo",open_demo)
    #cv.imwrite("lift_door_line_detection_only_straight.png",open_demo)!!!

def line_detection_demo(image):
    #cv.imshow("ori_part",image)
    edges = cv.Canny(image,60,80,apertureSize = 3)#上下限改成25,120，可以降低直线识别的门槛
    open_demo(edges)

cap = cv.VideoCapture(r"C:\Users\ningningbeibei33\Desktop\graduate\1\a\b\c\data\lift_video_10_2.mp4")
count = 0
#cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)

fourcc1 = cv.VideoWriter_fourcc(*'XVID')
fps1 = cap.get(cv.CAP_PROP_FPS)
size1 = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out1 = cv.VideoWriter("C:/Users/ningningbeibei33/Desktop/graduate/1/a/b/c/data/door_line/binary_threshold_2.avi",fourcc1, fps1, size1)

#while count < 30*110:
#    ret, frame = cap.read()
#    count = count + 1
open_frame_count = 0
alert_label = ""

while True:
    ret, frame = cap.read()
    count = count + 1
    if ret == False:
        break;
    lift_door = frame
    lift_door_part = lift_door[40:120,500:800] #[40:120,500:800]是门上部的范围
    
    #cv.imshow("lift_door_all",lift_door)
    #cv.imshow("lift_door_part",lift_door_part) #显示上部分无人的门区域
    lift_door_part_inv = inverse_image_demo(lift_door_part)
    #cv.imshow("lift_door_part_inv",lift_door_part_inv)
    processed_lift = contrast_brightness_demo(lift_door_part_inv,3,0)
    #cv.imshow("processed_lift",processed_lift)
    binary_threshold = threshold_demo(processed_lift)

    #统计二值化图像中所有像素的值（255或0），然后统计num_black=黑色的像素点个数，即门打开的区域面积。
    height, width = binary_threshold.shape
    sum_pixel = 0
    for row in range(height):
        for col in range(width):
            sum_pixel = sum_pixel + binary_threshold[row][col]
    num_black = int(height*width - sum_pixel/255)
    #print("binary_threshold # shape = ",binary_threshold.shape)
    #print("sum_pixel = ",sum_pixel)
    print("num_black = ",num_black)
    #print("binary_threshold = ",binary_threshold)

    if num_black>100:
        label = "The door is OPEN"
        is_open = 1 #is_open=1为开，需要开始计帧数，超过阈值需要报警
    else:
        label = "The door is CLOSED"
        is_open = 0
    print("count = ",count)
    
    if is_open:
        open_frame_count = open_frame_count + 1
        if open_frame_count > 30*13: #门打开的时间超过13秒，29.97帧/秒，就会显示报警文字
            alert_label = "Alert! The door has been open for too long time!"
            print("ALERT!!!")
    else:
        open_frame_count = 0
        alert_label = ""

    cv.putText(frame, label, (50, 30), cv.FONT_HERSHEY_SIMPLEX, 0.70, (0,0,255), 2)
    cv.putText(frame, alert_label, (50, 80), cv.FONT_HERSHEY_SIMPLEX, 0.70, (0,0,255), 2)
    
    out1.write(frame)
    cv.imshow("OPEN_CLOSED",frame)

cv.waitKey(0) # 等有键输入或者1000ms后自动将窗口消除，0表示只用键输入结束窗口
cv.destroyAllWindows()  # 关闭所有窗口
