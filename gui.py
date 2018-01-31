import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

import capture

DEBUG = True
app = QApplication(sys.argv)


def DEBUG_LOG(message):
    if DEBUG:
        print("[DEBUG] " + message)


class UpdateThread(QThread):
    pix_map_signal = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.stream = capture.VideoStream()
        DEBUG_LOG("UpdateThread Initialized")

    def run(self):
        DEBUG_LOG("UpdateThread Running")
        while True:
            # Change to stream.get_next_frame_raw() for raw Image from camera
            frame = self.stream.get_next_frame()

            # Convert image
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            image = QPixmap.fromImage(image)

            # TODO: make rescale size dynamic as gui gets stretched
            rescaled_image = image.scaled(520, 360, Qt.KeepAspectRatio)
            self.pix_map_signal.emit(rescaled_image)

        DEBUG_LOG("UpdateImage Thread out of infinite loop o.O?, u fucked up")

    def stop(self):
        self.stream.destroy()
        self.terminate()
        DEBUG_LOG("UpdateImage Thread Stopped")


class GUI(QWidget):
    def __init__(self, window_title='Virtual Piano'):
        QWidget.__init__(self)
        self.setWindowTitle(window_title)
        self.layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()

        self.lbl_image = QLabel(self)
        self.lbl_image.resize(520, 360)

        self.lbl_keys = QLabel(self)
        self.lbl_keys.setPixmap(QPixmap("res/keys.png").scaledToWidth(520))
        self.lbl_keys.resize(520, 360)

        self.thread = UpdateThread(self)
        self.thread.pix_map_signal.connect(self.lbl_image.setPixmap)
        self.thread.start()

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.destroy)

        self.inner_layout.addWidget(self.lbl_image)
        self.inner_layout.addWidget(self.lbl_keys)

        self.layout.addLayout(self.inner_layout)
        self.layout.addWidget(self.btn_exit)

        self.setLayout(self.layout)
        DEBUG_LOG("GUI Initialized")

    def run(self):
        self.show()
        app.exec_()
        self.destroy()

    def destroy(self):
        self.thread.stop()
        exit()


def main():
    ui = GUI()
    ui.run()


if __name__ == "__main__":
    main()
