"""
这个类用来获取网络上的图片

"""
from PyQt5.QtCore import QThread, pyqtSignal
import src.window_assembly.Widget as Widget
from src.get_web_image.GetWebTool import *

imageURL = []


class GetImageThead(QThread):
    column = 5  # 定义表格行数
    update_image = pyqtSignal(bytes, int)  # 定义一个更新UI的信号量
    add_row = pyqtSignal()  # 定义一个创建新行的信号量
    clear_table = pyqtSignal()  # 定义一个清空表格的信号量
    loaded = pyqtSignal()  # 定义一个加载完毕信号量

    def run(self):
        global imageURL
        self.getImageURL()
        tempCount = Widget.loadImageCount

        for i in range(6):
            self.add_row.emit()  # 发送创建新行的信号
            for j in range(tempCount + self.column * i, tempCount + self.column * (i + 1)):
                if j >= len(imageURL):
                    break
                res = requests.get(imageURL[j])
                self.update_image.emit(res.content, j % self.column)  # 发送更改UI的信号
                # 更新加载图片总数
                Widget.loadImageCount += 1
            if Widget.loadImageCount % 5 != 0:
                self.loaded.emit()  # 发送加载完毕信号
                break

    def getImageURL(self):
        global imageURL
        htmlDate = None
        # 如果已经加载图片的数量不是30的倍数，则补全为30的倍数
        tempCount = Widget.loadImageCount if Widget.loadImageCount % 30 == 0 else \
            Widget.loadImageCount + 30 - Widget.loadImageCount % 30
        # 通过一个死循环获取图片，如果图片获取失败就改变数据重新获取
        while htmlDate is None:
            htmlDate = getWebDate('https://image.baidu.com/search/acjson?',
                                  Widget.requestDate.format(tempCount))  # 获得网络数据
            tempCount += 30

        for i in range(len(htmlDate) - 1):
            url = htmlDate[i]['thumbURL']
            imageURL.append(url)  # 将图片链接加入列表
