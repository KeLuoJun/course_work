import torch
import gradio as gr
import cv2
import numpy as np

base_conf = 0.25
base_iou = 0.45

# 加载自定义YOLOv5模型
model = torch.hub.load("./", 'custom', path="./runs/train/exp3/weights/best.pt", source='local')

title = "黑猴VS小白龙"

description = "训练后的模型，用于识别黑猴和小白龙。"


def predict_live(video_path, conf, iou):
    model.conf = conf
    model.iou = iou

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Video file cannot be opened")
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame).render()[0]

        frames.append(results)

        yield results
    cap.release()



# 启动Gradio接口
gr.Interface(inputs=[gr.Video(), # 调用组件gr.Image()，用于接收图像输入 
                    #  gr.Webcam()  # 调用组件gr.Webcam()，用于接收摄像头输入
                     gr.Slider(minimum=0, maximum=1, value=base_conf), 
                     gr.Slider(minimum=0, maximum=1, value=base_iou)],  
             outputs="image",    # 也可以输入"image"调用gr.Image()组件 
             fn=predict_live,
             title=title,
             description=description,
             live=True,  # 实时更新,之后没有submit按钮
             examples=[
                 ["./datasets/images/train/4800.jpg", base_conf, base_iou],
                 ["./datasets/images/train/4830.jpg", base_conf, base_iou],
                 ["./datasets/images/train/4890.jpg", base_conf, base_iou],
             ]).launch(share=False)  # share=True,生成公网地址
