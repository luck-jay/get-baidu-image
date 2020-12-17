"""

这是这个程序的主窗口，这个窗口实现了这个程序所有的功能。

1. 把从百度图库爬取的图片显示到窗口上。
2. 下载图片。
3. 配合爬虫，用可视化的方法去操作爬虫，爬取图片。

"""

from PyQt5.QtWidgets import QWidget, QMenu, QHBoxLayout, QVBoxLayout, QTableWidget, QPushButton, QLineEdit, \
    QAbstractItemView, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QCursor
from PyQt5.QtCore import Qt
from src.window_assembly.GetImageThead import GetImageThead
import src.window_assembly.GetImageThead as GetImage
import urllib.request

loadImageCount = 0  # 定义已加载图片的数量
requestDate = ''  # 定义请求数据


class Widget(QWidget):
    column = 5  # 记录表格的列总数
    rowCurrent = -1  # 记录表格当前应该在第几行显示信息
    saveImageCount = 0  # 记录当前保存图片总数
    flagLoaded = False
    requestDateMould = 'tn=resultjson_com&ipn=rj&fp=result&ie=utf-8&oe=utf-8&word={0}&pn={1}&rn=30'  # 请求数据模板

    def __init__(self, path='./'):
        """

        创建出需要用到的布局，以及需要用到的按钮等控件。

        """
        super(Widget, self).__init__()
        # 创建一个线程用于获取网络上的图片
        self.getImageThead = GetImageThead()
        # 得到文件保存路径
        self.filePath = path
        # 设置右键单击时获得图片的默认数据
        self.imageSaveData = None
        # 创建一个菜单
        self.contextMenu = QMenu()
        # 为右键菜单添加动作
        self.actionSave = self.contextMenu.addAction('保存')
        # 创建一个水平布局
        self.headLayout = QHBoxLayout()
        # 创建一个垂直布局
        self.bodyLayout = QVBoxLayout()
        # 创建一个表格
        self.tableWidget = QTableWidget()
        # 创建一个获取图片用的按钮
        self.getImageButton = QPushButton('获取图片')
        # 创建一个文本输入框
        self.textEdit = QLineEdit()
        # 创建一个刷新按钮
        self.refreshButton = QPushButton('刷新')
        # 界面初始化函数
        self.initUI()

    def initUI(self):
        """

            实现了窗口UI的设计，对界面的布局进行设计。

        """
        # 设计表格
        self.tableWidget.setColumnCount(self.column)
        # 设置表格列的宽度
        for i in range(5):
            self.tableWidget.setColumnWidth(i, 355)
        # 设置表格不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置隐藏表格水平头和垂直头
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        # 设置隐藏表格线
        self.tableWidget.setShowGrid(False)
        # 得到表格的滚动条对象
        scrollBar = self.tableWidget.verticalScrollBar()
        # 将信号和槽绑定
        self.getImageButton.clicked.connect(self.onClick_getImageButton)  # 单击信号
        self.refreshButton.clicked.connect(self.clearTable)  # 单击信号
        self.actionSave.triggered.connect(self.save)  # 选择信号
        self.getImageThead.update_image.connect(self.updateUI)  # 更新界面信号
        self.getImageThead.add_row.connect(self.newRow)  # 添加行信号
        self.getImageThead.clear_table.connect(self.clearTable)  # 清空表格信号
        scrollBar.valueChanged.connect(self.scrollTest)  # 滚动条被拖动信号
        self.getImageThead.loaded.connect(self.imageLoaded)
        # 添加到布局中
        self.headLayout.addWidget(self.textEdit)
        self.headLayout.addWidget(self.getImageButton)
        self.headLayout.addWidget(self.refreshButton)
        self.bodyLayout.addLayout(self.headLayout)
        self.bodyLayout.addWidget(self.tableWidget)

        # 把布局加入到窗口中
        self.setLayout(self.bodyLayout)

    def onClick_getImageButton(self):
        """

            这个方法是当获取图片按钮单击的时候，操作网络爬虫爬取图片，并把网络爬虫爬取的图片显示到主 窗口上。

        """
        global requestDate
        # 清空表格
        self.clearTable()
        # 判断是否输入搜索内容
        if self.textEdit.text() == '':
            QMessageBox.information(self, '提示信息', '请先输入搜索内容', QMessageBox.Ok)
        else:
            #  清空之前的缓存
            GetImage.imageURL.clear()
            requestDate = self.requestDateMould.format(self.textEdit.text(), '{}')  # 更改搜索内容
            self.getImageThead.start()  # 启动线程开始获取图片

    def updateUI(self, image, y):
        """
        这个方法用来更新界面UI，通过线程发送的信号来更新UI
        :param image: 为图片数据
        :param y: 为显示位置的y坐标
        """
        global loadImageCount  # 载入全局变量
        # 获得图片
        image = QImage.fromData(image)
        label = QLabel()
        # 当右键单击时显示菜单
        label.customContextMenuRequested.connect(self.showContextMenu)
        label.setContextMenuPolicy(Qt.CustomContextMenu)
        label.setToolTip(str(loadImageCount))
        # label.setAcceptDrops(True)  # 设置可拖动
        # 设置图片大小为300x300
        label.setPixmap(QPixmap(image).scaled(350, 350, Qt.KeepAspectRatio))
        # 把图片加入到表格中
        self.tableWidget.setCellWidget(self.rowCurrent, y, label)

    def clearTable(self):
        """
        点击刷新按钮的时候调用这个方法清空表格

        """
        global loadImageCount
        # 刷新表格后显示的数据清零
        loadImageCount = 0
        for i in range(self.rowCurrent + 1, -1, -1):
            self.tableWidget.removeRow(i)  # 删除表格指定行
        self.rowCurrent = -1  # 重置表格行现在位置

    def showContextMenu(self):
        """
        右键点击时调用的方法

        """
        # 获得单击的图片
        self.imageSaveData = self.sender().toolTip()

        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def save(self):
        """
        当用户选择保存时调用这个方法保存图片

        """
        url = GetImage.imageURL[int(self.imageSaveData) - 1]  # 获得需要保存图片的URL
        # self.imageSaveData.save(self.filePath + 'image_%04d.jpg' % self.saveImageCount, 'jpg', 100)  # 保存最佳质量的图片

        # 浏览器访问头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/64.0.3282.168 Safari/537.36'}

        try:
            req = urllib.request.Request(url, headers=headers)  # 创建Request对象
            response = urllib.request.urlopen(req, timeout=10)
            imageDate = response.read()
            # 把图片保存到文件中
            with open(self.filePath + 'image_%04d.jpg' % self.saveImageCount, 'wb') as f:
                f.write(imageDate)

            # 总保存图片数更新
            self.saveImageCount += 1
        except Exception:
            print('请求超时,图片保存失败')

    def newRow(self):
        """
        创建一个新的表格行

        """
        self.rowCurrent += 1  # 行计数加1

        self.tableWidget.insertRow(self.tableWidget.rowCount())  # 创建一个新行
        # 设置行宽度
        self.tableWidget.setRowHeight(self.rowCurrent, 355)

    def setPath(self):
        """
            设置文件保存路径

        """
        self.filePath = QFileDialog.getExistingDirectory(self, '选择文件夹', '.')

    def scrollTest(self):
        """
        判断滚动条是否到达窗口底部，如果到达，就继续加载新的内容

        """
        # 获取滚动条当前值，并判断滚动条是否到达窗口底部附件5个单元格内,并且图片没有加载完毕，则继续加载图片，否则不加载
        if self.sender().value() > self.rowCurrent - 5 & self.flagLoaded == False:
            self.getImageThead.start()  # 继续加载图片

    def imageLoaded(self):
        """
        当图片加载完毕调用这个方法提醒
        :return:
        """
        QMessageBox.information(self, '完毕', '图片加载完成，没有更多图片了！', QMessageBox.Ok)
        # 设置标志位为真，表示已经加载完毕
        self.flagLoaded = True
