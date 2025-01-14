# 导入必要的库
import torch
import cv2
import queue
import threading
import numpy as np


class FrameCapture(threading.Thread):
    def __init__(self, input_queue, camera_id=0):
        super().__init__()
        self.input_queue = input_queue
        self.camera_id = camera_id
        self.stopped = False
        
    # 捕获帧并将其放入输入队列
    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        cap.set(cv2.CAP_PROP_FPS, 60)
        
        while not self.stopped:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            if self.input_queue.full():
                try:
                    self.input_queue.get_nowait()
                except queue.Empty:
                    pass
            
            self.input_queue.put(frame)
            
        cap.release()

    # 停止帧捕获
    def stop(self):
        self.stopped = True

# 定义一个执行YOLO模型推理的线程类
class YOLOInference(threading.Thread):
    def __init__(self, input_queue, output_queue, model_path='./yolov5s.pt'):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.stopped = False
        
        # 加载模型
        self.model = torch.hub.load("./", "custom", path=model_path, source='local')
        if torch.cuda.is_available():
            self.model.cuda()
        self.model.conf = 0.30
        self.model.iou = 0.45
        self.model.eval()
        
    def run(self):
        while not self.stopped:
            try:
                frame = self.input_queue.get(timeout=1.0)
                
                results = self.model(frame)
                processed_frame = results.render()[0]
                
                self.output_queue.put(processed_frame)
                
            except queue.Empty:
                continue

    # 停止推理
    def stop(self):
        self.stopped = True

# 定义一个显示处理后帧的线程类
class DisplayOutput(threading.Thread):
    def __init__(self, output_queue):
        super().__init__()
        self.output_queue = output_queue
        self.stopped = False
        
    def run(self):
        while not self.stopped:
            try:
                frame = self.output_queue.get(timeout=1.0)
                
                cv2.imshow('object detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stopped = True
                    
            except queue.Empty:
                continue
                
    # 停止显示
    def stop(self):
        self.stopped = True

def main():
    # 创建队列
    input_queue = queue.Queue(maxsize=30)  
    output_queue = queue.Queue()
    
    camera_id = 1  # 替换为实际摄像头ID
    capture_thread = FrameCapture(input_queue, camera_id=camera_id)
    capture_thread.start()
    
    # 创建并启动多个YOLO推理线程
    num_inference_threads = 3  # 可以根据需要调整线程数量
    inference_threads = []
    for _ in range(num_inference_threads):
        inference_thread = YOLOInference(input_queue, output_queue)
        inference_thread.start()
        inference_threads.append(inference_thread)
    
    # 创建并启动显示线程
    display_thread = DisplayOutput(output_queue)
    display_thread.start()
    
    try:
        # 等待显示线程结束（当按下q键时）
        display_thread.join()
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        display_thread.stop()
        capture_thread.stop()
        for thread in inference_threads:
            thread.stop()
        
        capture_thread.join()
        for thread in inference_threads:
            thread.join()
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()