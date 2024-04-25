import cv2
from tqdm import tqdm
import os

"""
parameters:
    video_path: the source video you want to crop to frames
    output_path: the dest dictory you want to save the cropped frames
function:
    crop the video to frames 
"""
def crop_face_use_cv2(video_path, output_path):
    current_frame = 0
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    output_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    output_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    output_fps    = fps  
    output_fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
    out = cv2.VideoWriter(output_path, output_fourcc, output_fps, (output_width, output_height))
    progress_bar  = tqdm(total=total_frames, desc="Processing Frames", unit="frame")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_index = current_frame + 1
        index_text  = f"Frame: {frame_index}"
        cv2.putText(frame, index_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        frame_output_path = os.path.join(output_path, f"frame_{frame_index:04d}.jpg")
        cv2.imwrite(frame_output_path, frame)
        current_frame += 1
        progress_bar.update(1)
    cap.release()
    out.release()

if __name__=="__main__":
    video_path = r"your source video abs path"
    output_path = r"your destination directory to save cropped frames"
    crop_face_use_cv2(video_path, output_path)