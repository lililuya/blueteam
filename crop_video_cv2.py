import cv2

# 视频路径
video_path = "l2.mp4"

# 打开视频
cap = cv2.VideoCapture(video_path)

# 获取视频的帧率和总帧数
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 设置输出视频的参数
output_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 输出视频的宽度
output_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 输出视频的高度
output_fps = fps  # 输出视频的帧率
output_fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 输出视频的编码格式

# 创建输出视频的写入器
output_path = "path/to/output.mp4"
out = cv2.VideoWriter(output_path, output_fourcc, output_fps, (output_width, output_height))

# 开始读取视频帧并进行保存
current_frame = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 生成当前帧的索引
    frame_index = current_frame + 1

    # 构建索引文本
    index_text = f"Frame: {frame_index}"

    # 在帧上绘制索引文本
    cv2.putText(frame, index_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 保存当前帧
    frame_output_path = f"73_part1/frame_{frame_index:04d}.jpg"
    cv2.imwrite(frame_output_path, frame)

    current_frame += 1

# 释放资源
cap.release()
out.release()