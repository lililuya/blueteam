import cv2
import os
from tqdm import tqdm

# This script is intented to resize the video frames
def resize_frame(path, out_dir, ratio):
    image_path_list = os.listdir(path)
    for item in tqdm(sorted(image_path_list)):
        item_path = os.path.join(path, item)
        item_basename = os.path.basename(os.path.splitext(item_path)[0])
        image = cv2.imread(item_path)
        
        # get the source frame size
        height = image.shape[0]
        width  = image.shape[1]
        size   = width, height
        
        # take ratio get dest size
        scale_size = size*ratio
        image_resize = cv2.resize(image, scale_size, interpolation=cv2.INTER_LANCZOS4)
        out_path = os.path.join(out_dir, item_basename + ".jpg")
        cv2.imwrite(out_path, image_resize)
    
if __name__=="__main__":
    path = "the selected frames in step2"
    out_dir = "the destination dictory save the resized frames"
    ratio = 0.5
    resize_frame(path, out_dir, ratio)