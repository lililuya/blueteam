import moviepy.editor as mpe
from tqdm import tqdm
import numpy as np
import  cv2
import  os

def crop_video(video_path = "./l2.mp4", root_dir = "./73_part1"):
    video = mpe.VideoFileClip(video_path)
    n_frames = int(np.floor(video.fps * video.duration))
    frames = video.iter_frames()
    frames = list(tqdm(frames, desc="Loading Frames", total=n_frames))
    for index, frame in enumerate(frames):
        fram_path_out = os.path.join(root_dir, f"{index}"+".png")
        frame = frame[...,::-1]
        cv2.imwrite(fram_path_out, frame)


if __name__=="__main__":
    crop_video()