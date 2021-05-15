# Visual-Surveillance-Analysis-and-Abnormality-Diagnosis-of-A-Elevator-Based-on-Machine-Learning-Beini
This is the video material and programming of graduation paper of Beining ZHANG majoring in Industrial Engineering in Zhejiang University.

The abstract of the paper is as following:

Lift is widely used in daily life scenes , such as residential areas, shopping malls and hospitals. How to count the real-time flow of people in the lift according to the lift monitoring video is a new field of intelligent image processing. Using background modeling and pattern recognition algorithms, the foreground and background of the lift can be separated. The type of the target object can be recognized, and the recognition accuracy rate can be marked. At the same time, it can identify the opening and closing state of the lift door, carry out intelligent diagnosis for some abnormal conditions. It will use the intelligent lift monitoring system to reduce the need of manual labor. 

In Chapter 1, the research background and significance of the dissertation were introduced. The research status of background modeling and pattern recognition in image recognition at home and abroad is comprehensively evaluated, including the existing algorithms and the main problems. Also, the main research contents of this paper are proposed. 

In Chapter 2, background modeling is carried out by two algorithms, MOG2 and KNN. The author compares their algorithm and implementation effects. Foreground target and lift background are separated to recognize the target. 

In Chapter 3, Yolov3 algorithm is used to the recognition of the flow of people in the lift. We judge the type of the object in the foreground, mark the recognition probability, and count the total number of people in each frame. 

In Chapter 4, we take the part of the lift monitoring video image which is not blocked by the flow of people, and get the binary image through a series of steps of image processing. According to the area of the black pixels in the image, we select num_black in the image at the moment when the door just opens as the threshold value to judge whether the lift door is open or closed in real time. At the same time, the alarm function is accomplished when the lift door has been open for too long time. 

In Chapter 5, the main research work of this thesis was summarized and future work was proposed.
