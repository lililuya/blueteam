import cv2
import os
from tqdm import tqdm

# This script is intented to resize the video frames
path = r"E:\blueteam\seleted_73_part1"
out_dir = r"E:\blueteam\seleted_73_part1_resize"
image_path_list = os.listdir(path)
for item in tqdm(sorted(image_path_list)):
    item_path = os.path.join(path, item)
    item_basename = os.path.basename(os.path.splitext(item_path)[0])
    image = cv2.imread(item_path)
    image_resize = cv2.resize(image, (480, 270), interpolation=cv2.INTER_LANCZOS4)
    out_path = os.path.join(out_dir, item_basename + ".jpg")
    cv2.imwrite(out_path, image_resize)
    
