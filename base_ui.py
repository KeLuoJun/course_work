import cv2
import sys
import torch
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
# QMainWindow: 提供了一个主应用程序窗口，可以包含菜单栏、工具栏、状态栏等组件。
# QApplication: 管理 GUI 应用程序的控制流和主要设置，每个使用 Qt 的应用程序都需要一个 QApplication 实例。
# QFileDialog: 提供一个对话框，让用户可以选择文件或目录，常用于打开和保存文件的操作。

from PySide6.QtGui import QPixmap, QImage
# QPixmap: 用于显示图像，支持多种图像格式，并且可以在屏幕设备上高效绘制。
# QImage: 提供了一个与平台无关的图像表示，可以进行图像处理操作。

from PySide6.QtCore import QTimer
# QTime: 提供了一个时间类，用于处理时间相关的操作，如获取当前时间、时间比较等。

from main_windows_ui import Ui_MainWindow


def convert2QImage(img):
    """
    将numpy数组图像转换为QImage对象。

    参数:
    img (numpy.ndarray): 一个三维的numpy数组，表示一幅图像。其shape属性包含图像的高度、宽度和通道数。

    返回:
    QImage: 一个QImage对象，用于在Qt图形界面上显示图像。
    """
    # 获取图像的高度、宽度和通道数
    height, width, channel = img.shape
    
    # 使用图像的数据、宽度、高度和字节跳转来创建QImage对象
    # 这里的字节跳转是宽度乘以通道数，因为QImage需要知道每一行像素的字节数
    # QImage.Format_RGB888指定图像的格式为RGB888，即每个像素由红、绿、蓝三个8位通道组成
    return QImage(img, width, height, width * channel, QImage.Format_RGB888)



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 初始化定时器
        self.timer = QTimer()
        # 设置定时器间隔为1毫秒
        self.timer.setInterval(0.1)
        self.video = None
        self.model = torch.hub.load("./", 'custom', path="./runs/train/exp3/weights/best.pt", source='local')
        
        self.bind_solts()

    def image_pred(self, file_path):
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)  # 使用IMREAD_COLOR，默认是BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将BGR图像转换为RGB图像
        results = self.model(img)
        image = results.render()[0]  # array
        return convert2QImage(image)
    
    def video_pred(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.input.setPixmap(QPixmap.fromImage(convert2QImage(frame)))

            results = self.model(frame)
            image = results.render()[0]  # array
            self.output.setPixmap(QPixmap.fromImage(convert2QImage(image)))



    def open_image(self):
        self.timer.stop()
        print("点击了图片检测！")
        file_path = QFileDialog.getOpenFileName(self, dir="./datasets/images/train",
                                                filter="*.jpg;*.png;*.jpeg")
        if file_path[0]:
            file_path = file_path[0]
            self.input.setPixmap(QPixmap(file_path)) # 把原图片显示在self.input组件上

            qimage = self.image_pred(file_path)
            # 把检测后的图片显示在self.output组件上
            self.output.setPixmap(QPixmap.fromImage(qimage))


    def open_video(self):
        print("点击了视频检测！")
        file_path = QFileDialog.getOpenFileName(self, dir="./datasets",
                                                filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            self.video = cv2.VideoCapture(file_path)
            self.timer.start()  # 启动定时器
                

    def bind_solts(self):
        self.det_image.clicked.connect(self.open_image)
        self.det_video.clicked.connect(self.open_video)
        # 将定时器的timeout信号连接到video_pred方法
        self.timer.timeout.connect(self.video_pred)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
    


