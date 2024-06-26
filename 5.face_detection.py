from insightface_func.face_detect_crop_single import Face_detect_crop
import cv2
import math
import numpy as np

def look_up_table(x_coordination, width, bin_num=60):
    if x_coordination<0:x_coordination=0
    if x_coordination>width:x_coordination=width-1
    cell = math.floor(x_coordination / width * bin_num)
    if cell >= 60:
        cell = 59
    return cell

def look_up_table_ang(ang):
    cell = math.floor(ang)
    return cell

eyes_list = []
index = 1

for eye_i in range(180):
    eye_i = cv2.imread("./images_man_0422/images/man{:04}.jpg".format(eye_i))
    eyes_list.append(eye_i)
    index += 1
# for eye_i in range(60):
#     eye_i = cv2.imread("./eyes_images/zuoyou%d.jpg"%index)
#     eyes_list.append(eye_i)
#     index += 1
# eyes_list = eyes_list[::-1]

mode = "none"
detect = Face_detect_crop(name='antelope', root='./insightface_func/models')
cap = cv2.VideoCapture(0)  # 打开摄像头

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))


detect.prepare(ctx_id = 0, det_thresh=0.6,\
                            det_size=(640,640), mode = mode)
point_size  = 1
point_color = (0, 0, 255) # BGR
thickness   = 4 #  0 、4、8
ori_point_y = height/2
ori_point_x = width/2
unit_vec    = [1,0]

while True:
    ret, frame = cap.read()  # 读取摄像头画面
    kps = detect.get(frame, crop_size=112)
    if kps is not None:
        vec_k = [kps[2,0], kps[2,1]]
        vec_k = [vec_k[0]-ori_point_x, vec_k[1]-ori_point_y]
        mod   = math.sqrt(vec_k[0]**2+vec_k[1]**2)
        angel = math.acos(vec_k[0] / mod)/math.pi * 180

        print("mod:", mod, "angle:", angel)
        cell = look_up_table_ang(angel)
        eyes = eyes_list[cell]
    #     cell = look_up_table(int(kps[2,0]),width)
    #     # print("position:",kps[2,1],"cell:",cell)
    #     print("position:", kps[2,0],"cell:",cell)
    #     # eyes = eyes_list[cell]
    #     # eyes = np.concatenate((eyes,eyes,eyes,eyes,eyes),axis=0)
    #     # eyes = np.concatenate((eyes,eyes,eyes,eyes,eyes),axis=1)
        cv2.imshow("Camera", eyes)  # 显示画面
    #     # print("frame shape:",frame.shape)
        
    #     # cv2.circle(
    #     #             frame, 
    #     #             (int(kps[2,0]), int(kps[2,1])), 
    #     #             point_size,
    #     #             point_color,
    #     #             thickness
    #     #         )

    # #     # print(detect_results)
    # #     # box = [int(box_i) for box_i in detect_results]
    # #     # color = (0, 0, 255)
    # #     # cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)


    # cv2.imshow("Camera", frame)  # 显示画面
 
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 按下 'q' 键退出循环
        break
 
cap.release()  # 关闭摄像头
cv2.destroyAllWindows()  # 销毁窗口