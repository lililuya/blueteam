# 😙Blueteam👍
some script for process data ❓ 

![Language](https://img.shields.io/badge/language-python-blueviolet)  ![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen)
## 1. Step pipeline scripts

### 1.1 Crop the video

+ Using the script `1.crop_video_cv2.py` as following:
  + Modify the parameters（Use absolute path）
    + **video_path**:  *the source video you want to crop to frames*
    + **output_path**： *the destination directory you want to save the cropped frames*
  + Run script
    + In current directory，type `python $your script name$` 
    + Example: `python 1.crop_video_cv2.py`
  + The result is located in **output_path**

### 1.2 Select the suitable cropped frames

+ How to choose? 🤔 
  + No blink
  + Widen eyes
  + Motion in time sequence
+ Use the script as following:
  + Modify the parameters
    + **duration**: *the slice of the cropped frames*
    + **image_list_path**: *your source cropped frames got from step1*
    + **out_dir**: *your destination directory to save the selected frames*

The result is located in **out_dir**

### 1.3 Resize the selected frames 

+ Why? 🤔 
  +  Fit the screen for playback
+ Use the script as following:
  + Modify the parameters
    + **path**: *the selected frames in step2*
    + **out_dir**: *the destination dictory save the resized frames*
    + **ratio**: *scaling ratio*
+ The result is located in **out_dir**

### 1.4 Crop Eye

+ Use the script as following:
  + Modify the parameters
    + **frame_path**: *the resized frames directory*
    + **out_dir**: *save eyes*
    + **ratio**: *from the top to bottom, as [ratio1 x height ,ratio2 x height ]*
  + The result is located in **out_dir**

### 1.5 Launch the program

+ replace the path as your cropped eye frames directory

## 2. End-to-end operation 

+ Modify parameters
  + as mentioned before
+ `python whole_pipeline_process.py`

