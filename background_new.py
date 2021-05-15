#生成视频的背景建模->黑白图像，但只有显示，没有保存文件，需要截屏
import cv2 as cv
import numpy as np

# 加载视频
cap = cv.VideoCapture(r"C:\Users\ningningbeibei33\Desktop\graduate\1\a\b\c\data\lift_video_10_2.mp4")
# 创建混合高斯模型用于背景建模
background_model = cv.createBackgroundSubtractorKNN() #或者使用cv.createBackgroundSubtractorMOG2()
background_model = cv.createBackgroundSubtractorMOG2()
# 形态学操作核
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

fourcc1 = cv.VideoWriter_fourcc(*'XVID')
fps1 =cap.get(cv.CAP_PROP_FPS)
size1 = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out1 = cv.VideoWriter("C:/Users/ningningbeibei33/Desktop/graduate/1/a/b/c/data/back_ground/BackgroundSubtractorKNN.avi",fourcc1, fps1, size1)
step = 0

while True:
    # 读取下一帧图像
    ret, frame = cap.read()
    # 更新模型参数，对预测结果进行开运算
    fgmask = background_model.apply(frame)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    # 轮廓筛选：人
    _, contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for ct in contours:
        perimeter = cv.arcLength(ct, True)
        if perimeter > 188:
            (x, y, w, h) = cv.boundingRect(ct)
            frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
    
    step = step + 1
    print("step = ",step)
    print(fgmask[20][20])
    cv.imshow("background",fgmask)
    background_show = cv.cvtColor(fgmask,cv.COLOR_GRAY2BGR)
    out1.write(background_show)

# 运行结束后的处理
cap.release()
cv.waitKey(0)
cv.destroyAllWindows()
