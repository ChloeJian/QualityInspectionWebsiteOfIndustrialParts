from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from demo import Ui_MainWindow
import sys
import cv2

x, y, w, h = 440, 160, 400, 400

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 1280)
        self.camera.set(4, 720)
        self.is_camera_opened = False  #30

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

    def Button_OpenCamera_Clicked(self):  # 打开和关闭摄像头
            self.is_camera_opened = ~self.is_camera_opened
            if self.is_camera_opened:
                self.Button_OpenCamera.setText("关闭摄像头")
                self._timer.start()
            else:
                self.Button_OpenCamera.setText("打开摄像头")
                self._timer.stop()

    def Button_Capture_Clicked(self):  # 捕获图片
        if not self.is_camera_opened:
            print("none")
            return

        self.captured1 = self.frame
        # Qt显示图片时，需要先转换成QImgage类型
        self.captured2 = cv2.cvtColor(self.captured1, cv2.COLOR_BGR2RGB)
        frame = self.captured2[y+1:y + h, x+1:x + w]  # 截取目标图片中从上到下161-560，从左到右441-840的区域
        frame = cv2.resize(frame, (256, 256))  # 图像大小为256*256
        cv2.imwrite('./test/good/000.png', frame)
        self.captured = cv2.imread('./test/good/000.png')
        self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.label_Capture.setPixmap(
            QPixmap.fromImage(QImg).scaled(self.label_Capture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    @QtCore.pyqtSlot()
    def _queryFrame(self):  # 循环捕获图片
        ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=1)
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.label_Camera.setPixmap(
                QPixmap.fromImage(QImg).scaled(self.label_Camera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.setWindowTitle("物体缺陷检测")
    window.show()
    sys.exit(app.exec_())
