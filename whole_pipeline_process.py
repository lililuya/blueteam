import cv2
from tqdm import tqdm
import os
import shutil
import numpy as np
from insightface_func.face_detect_crop_multi import Face_detect_crop

"""为了避免内存不够，每步都保存中间结果"""

class ProcessData():
    def __init__(self, 
                 video_path, 
                 cropped_dir, 
                 selected_dir, 
                 resized_dir, 
                 cropped_eye_dir, 
                 resized_ratio, 
                 ratio_start,
                 ratio_end, 
                 duration) -> None:
        self.video_path  = video_path
        self.cropped_dir = cropped_dir
        self.seleted_dir = selected_dir
        self.resized_dir = resized_dir
        self.cropped_eye_dir = cropped_eye_dir
        
        self.resized_ratio = resized_ratio
        self.crop_eye_ratio = ratio_start, ratio_end
        self.duration    = duration
        
        self.face_detection = Face_detect_crop(name='antelope', root='./insightface_func/models')
        self.face_detection.prepare(ctx_id=0, det_thresh=0.6, det_size=(640, 640), mode=None, crop_size=384, ratio=0.8)
        
    def crop_face_use_cv2(self):
        current_frame = 0
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        output_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        output_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
        output_fps    = fps  
        output_fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
        out = cv2.VideoWriter(self.cropped_dir, output_fourcc, output_fps, (output_width, output_height))
        progress_bar  = tqdm(total = total_frames, desc="Processing Frames", unit="frame")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_index = current_frame + 1
            index_text  = f"Frame: {frame_index}"
            cv2.putText(frame, index_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            frame_output_path = os.path.join(self.cropped_dir, f"frame_{frame_index:04d}.jpg")
            cv2.imwrite(frame_output_path, frame)
            current_frame += 1
            progress_bar.update(1)
        cap.release()
        out.release()
    
    def random_seletct_image(self):
        image_list = sorted(os.listdir(self.cropped_dir))
        for i in range(0,len(image_list), self.duration):
            image_path = image_list[i]
            image_path = os.path.join(self.cropped_dir, image_path)
            image_basename = os.path.basename(os.path.splitext(image_path)[0])
            out_path = os.path.join(self.seleted_dir, image_basename + ".jpg")
            shutil.copy(image_path, out_path)

    def resize_frame(self):
        image_path_list = os.listdir(self.seleted_dir)
        for item in tqdm(sorted(image_path_list)):
            item_path = os.path.join(self.seleted_dir, item)
            item_basename = os.path.basename(os.path.splitext(item_path)[0])
            image = cv2.imread(item_path)
            
            # get the source frame size
            height = image.shape[0]
            width  = image.shape[1]
            size   = width, height
            
            # take ratio get dest size
            scale_size = size*self.resized_ratio
            image_resize = cv2.resize(image, scale_size, interpolation=cv2.INTER_LANCZOS4)
            out_path = os.path.join(self.resized_dir, item_basename + ".jpg")
            cv2.imwrite(out_path, image_resize)

    def get_eye_frame(self):
        for frame in tqdm(sorted(os.listdir(self.resized_dir)),"processed bar:"):
            frame_path = os.path.join(self.resized_dir, frame)
            ratio_start, ratio_end = self.crop_eye_ratio
            img_basename = os.path.basename(os.path.splitext(frame_path)[0])
            img = cv2.imread(frame_path)
            bboxes = self.face_detection.get_bboxes(img)
            bboxes = (bboxes[0])
            # from ratio_start to ratio_end
            img_cropped = img[int(bboxes[1]): int(bboxes[3]), int(bboxes[0]): int(bboxes[2]), :]
            # width = bboxes[0][2] - bboxes[0][0]
            # height = bboxes[0][3] - bboxes[0][1]
            # cv2.imwrite("test_crop.png", img_cropped)
            start_index = int(ratio_start*img_cropped.shape[0])
            end_index   = int(ratio_end*img_cropped.shape[0])
            img_cropped_eye = img_cropped[start_index: end_index , : , :]
            out_path = os.path.join(self.cropped_eye_dir, img_basename + ".png")
            cv2.imwrite(out_path, img_cropped_eye)
    
    def __call__(self,):
        self.crop_face_use_cv2()
        self.random_seletct_image()
        self.resize_frame()
        self.get_eye_frame()

if __name__=="__main__":
    
    video_path      = ""
    cropped_dir     = "" 
    selected_dir    = ""
    resized_dir     = ""
    cropped_eye_dir = ""
    resized_ratio   = ""
    ratio_start     = ""
    ratio_end       = ""
    duration        = ""
    
    data_model      = ProcessData(video_path,
                                  cropped_dir,
                                  selected_dir,
                                  resized_dir,
                                  cropped_eye_dir,
                                  resized_ratio,
                                  ratio_start,
                                  ratio_end,
                                  duration)
       
    data_model()