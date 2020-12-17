from src.window_assembly.Widget import Widget
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 设置一个文件保存路径
        self.path = './'
        # 创建一个滚动条
        # self.scrollArea = QScrollArea(self)
        self.w = Widget(self.path)
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('获取图片')
        # 得到屏幕坐标系
        deskTopWidget = QDesktopWidget().screenGeometry()
        # 设置窗口尺寸
        self.resize(deskTopWidget.width() - 100, deskTopWidget.height() - 100)
        # # 把窗口移动到屏幕正中央
        self.move((deskTopWidget.width() - self.width()) / 2, 50)

        # self.scrollArea.setWidget(self.w)
        self.w.setMaximumSize(self.width(), self.height())  # 设置窗口的高度和宽度为屏幕的宽度和高度
        # 获得菜单栏
        menuBar = self.menuBar()
        # 为菜单栏添加一个菜单项
        setting = menuBar.addMenu('设置')
        setting.addAction('更改路径')  # 为菜单栏添加一个动作

        setting.triggered.connect(self.w.setPath)  # 点击了这个动作触发

        self.setCentralWidget(self.w)  # 添加主窗口的中央控件


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
