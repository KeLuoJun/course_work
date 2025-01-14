### Python 期末课程作业：基于摄像头的图像处理

#### 主要功能实现：

- **手势识别**：使用 Google MediaPipe 实现。
- **虚拟键盘控制**：通过手势识别控制虚拟键盘。
- **YOLOv5 目标检测**：实时检测物体。
- **模型微调**：扩展 YOLOv5 模型以检测特定场景（如悟空与小白龙打斗）。

#### 文件结构：

```bash
project_root/
├── gesture_recognition/
│   ├── gesture_recognition.ipynb  # 手势识别代码
│   └── control_virtual_kb.ipynb   # 虚拟键盘控制代码
├── base_ui.py                     # 微调 YOLOv5 模型的 UI 展示 (PyQt5)
├── gradio_demo.py                 # 微调 YOLOv5 模型的 Gradio 展示
└── retrieve_camera.py             # 实时目标检测代码
```

#### 技术要点：

- **手势识别与虚拟键盘控制**：基于 Google MediaPipe 库。
- **实时目标检测**：采用多线程技术以适应无独显环境。
- **UI 界面**：使用 PyQt5 构建用户界面。

#### 详细说明：

1. **手势识别**

   - 文件：`gesture_recognition/gesture_recognition.ipynb`
   - 功能：利用 MediaPipe 进行手势识别。

2. **虚拟键盘控制**

   - 文件：`gesture_recognition/control_virtual_kb.ipynb`
   - 功能：通过手势识别结果控制虚拟键盘。

3. **YOLOv5 目标检测**

   - 文件：`retrieve_camera.py`
   - 功能：实现实时目标检测，并支持多线程处理以提高性能。

4. **模型微调**
   - 文件：`base_ui.py` 和 `gradio_demo.py`
   - 功能：提供两种不同的展示方式（PyQt5 和 Gradio），用于微调 YOLOv5 模型并展示检测结果。
