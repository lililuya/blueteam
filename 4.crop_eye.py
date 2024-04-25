import moviepy.editor as mpe
from tqdm import tqdm
import numpy as np
from insightface_func.face_detect_crop_multi import Face_detect_crop
import  cv2
import  os

class Eye_crop:
    def __init__(self,):
        self.face_detection = Face_detect_crop(name='antelope', root='./insightface_func/models')
        self.face_detection.prepare(ctx_id=0, det_thresh=0.6, det_size=(640, 640), mode=None, crop_size=384, ratio=0.8)
    
    def crop_video(self, video_path, root_dir):
        video = mpe.VideoFileClip(video_path)
        n_frames = int(np.floor(video.fps * video.duration))
        frames = video.iter_frames()
        frames = list(tqdm(frames, desc="Loading Frames", total=n_frames))
        for index, frame in enumerate(frames):
            fram_path_out = os.path.join(root_dir, f"{index}"+".png")
            frame = frame[...,::-1]
            cv2.imwrite(fram_path_out, frame)

    def test_single_image(self, img_path, out_dir, ratio):
        ratio_start, ratio_end = ratio
        img_basename = os.path.basename(os.path.splitext(img_path)[0])
        img = cv2.imread(img_path)
        bboxes = self.face_detection.get_bboxes(img)
        bboxes = (bboxes[0])
        # from ratio_start to ratio_end
        img_cropped = img[int(bboxes[1]): int(bboxes[3]), int(bboxes[0]): int(bboxes[2]),:]
        # width = bboxes[0][2] - bboxes[0][0]
        # height = bboxes[0][3] - bboxes[0][1]
        # cv2.imwrite("test_crop.png", img_cropped)
        start_index = int(ratio_start*img_cropped.shape[0])
        end_index   = int(ratio_end*img_cropped.shape[0])
        img_cropped_eye = img_cropped[start_index: end_index , : , :]
        out_path = os.path.join(out_dir, img_basename + ".png")
        cv2.imwrite(out_path, img_cropped_eye)

if __name__=="__main__":
    frame_path = "the resized frames directory"
    out_dir = "save eyes"
    ratio = 0.25, 0.75  # from the top to bottom
    crop_model = Eye_crop()
    for frame in tqdm(sorted(os.listdir(frame_path)),"processed bar:"):
        frame_path = os.path.join(frame_path, frame)
        crop_model.test_single_image(frame_path, out_dir, ratio)
