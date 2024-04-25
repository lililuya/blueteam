import shutil
import os


def random_seletct_image(image_list_path, out_dir, duration = 35):
    image_list = sorted(os.listdir(image_list_path))
    for i in range(0,len(image_list), duration):
        image_path = image_list[i]
        image_path = os.path.join(image_list_path, image_path)
        image_basename = os.path.basename(os.path.splitext(image_path)[0])
        out_path = os.path.join(out_dir, image_basename + ".jpg")
        shutil.copy(image_path, out_path)


if __name__=="__main__":
    duration = 30  # the duration of chose frames
    image_list_path = r"your source cropped frames got from step1 "
    out_dir = r"your destination directory to save the selected frames"
    random_seletct_image(image_list_path, out_dir, duration)