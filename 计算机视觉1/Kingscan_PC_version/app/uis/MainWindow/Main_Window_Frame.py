from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtGui,QtCore
from uis.components.myplot import static_fig
from uis.components.pltToolbar import NavigationToolbar2QTself
from uis.MainWindow.Main_Window_ui import Ui_MainWindow
import matplotlib.pyplot as plt



class Main_Window(QMainWindow):
    def __init__(self):
        super(Main_Window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        font = QtGui.QFont()
        font.setPointSize(9)

        self.fig1 = static_fig()
        self.fig_ntb1 = NavigationToolbar2QTself(self.fig1, self)
        self.fig_ntb1.setFont(font)
        self.ui.initial_img.addWidget(self.fig_ntb1)
        self.ui.initial_img.addWidget(self.fig1)
        self.fig1.ax1 = plt.subplot2grid((1, 1), (0, 0))
        self.fig1.ax1.axis('off')

        _translate = QtCore.QCoreApplication.translate
        # 添加tooltip
        self.ui.treeWidget_2.topLevelItem(0).setToolTip(0, _translate("MainWindow", "基础算法工具箱"))
        self.ui.treeWidget_2.topLevelItem(0).child(0).setToolTip(0, _translate("MainWindow", "图像增亮"))
        self.ui.treeWidget_2.topLevelItem(0).child(1).setToolTip(0, _translate("MainWindow", "图像暗化"))
        self.ui.treeWidget_2.topLevelItem(0).child(2).setToolTip(0, _translate("MainWindow", "生成灰度图"))
        self.ui.treeWidget_2.topLevelItem(0).child(3).setToolTip(0, _translate("MainWindow", "生成黑白图"))

        self.ui.treeWidget_2.topLevelItem(1).setToolTip(0, _translate("MainWindow", "对图片使用基于直方图操作的算法"))
        self.ui.treeWidget_2.topLevelItem(1).child(0).setToolTip(0, _translate("MainWindow", "SSR去阴影算法"))
        self.ui.treeWidget_2.topLevelItem(1).child(1).setToolTip(0, _translate("MainWindow", "直方图全局均衡化"))
        self.ui.treeWidget_2.topLevelItem(1).child(2).setToolTip(0, _translate("MainWindow", "限制对比度自适应直方图均衡化"))
        self.ui.treeWidget_2.topLevelItem(1).child(3).setToolTip(0, _translate("MainWindow", "YUV空间进行Clahe"))

        self.ui.treeWidget_2.topLevelItem(2).setToolTip(0, _translate("MainWindow", "对图片使用基于卷积核的算法"))
        self.ui.treeWidget_2.topLevelItem(2).child(0).setToolTip(0, _translate("MainWindow", "模糊"))
        self.ui.treeWidget_2.topLevelItem(2).child(1).setToolTip(0, _translate("MainWindow", "平滑"))
        self.ui.treeWidget_2.topLevelItem(2).child(2).setToolTip(0, _translate("MainWindow", "模板增强锐化"))
        self.ui.treeWidget_2.topLevelItem(2).child(3).setToolTip(0, _translate("MainWindow", "USM算法增强锐化"))
        self.ui.treeWidget_2.topLevelItem(2).child(4).setToolTip(0, _translate("MainWindow", "边缘增强"))
        self.ui.treeWidget_2.topLevelItem(2).child(5).setToolTip(0, _translate("MainWindow", "边缘增强超级版"))
        self.ui.treeWidget_2.topLevelItem(2).child(6).setToolTip(0, _translate("MainWindow", "轮廓获取"))
        self.ui.treeWidget_2.topLevelItem(2).child(7).setToolTip(0, _translate("MainWindow", "边缘检测"))

        self.ui.treeWidget_2.topLevelItem(3).setToolTip(0, _translate("MainWindow", "对图片使用二值化算法（均针对彩图）"))
        self.ui.treeWidget_2.topLevelItem(3).child(0).setToolTip(0, _translate("MainWindow", "Otsu"))
        self.ui.treeWidget_2.topLevelItem(3).child(1).setToolTip(0, _translate("MainWindow", "移动平均"))
        self.ui.treeWidget_2.topLevelItem(3).child(2).setToolTip(0, _translate("MainWindow", "自适应阈值处理"))
        self.ui.treeWidget_2.topLevelItem(3).child(3).setToolTip(0, _translate("MainWindow", "Sauvola最强二值化算法"))

        self.ui.treeWidget_2.topLevelItem(4).setToolTip(0, _translate("MainWindow", "对图片使用形态学方法处理"))
        self.ui.treeWidget_2.topLevelItem(4).child(0).setToolTip(0, _translate("MainWindow", "对图片进行腐蚀"))
        self.ui.treeWidget_2.topLevelItem(4).child(1).setToolTip(0, _translate("MainWindow", "对图片进行膨胀"))
        self.ui.treeWidget_2.topLevelItem(4).child(2).setToolTip(0, _translate("MainWindow", "对图片进行开运算"))
        self.ui.treeWidget_2.topLevelItem(4).child(3).setToolTip(0, _translate("MainWindow", "对图片进行闭运算"))
        self.ui.treeWidget_2.topLevelItem(5).setToolTip(0, _translate("MainWindow", "对图片施加炫酷滤镜效果"))
        self.ui.treeWidget_2.topLevelItem(5).child(0).setToolTip(0, _translate("MainWindow", "对图片施加复古特效"))
        self.ui.treeWidget_2.topLevelItem(5).child(1).setToolTip(0, _translate("MainWindow", "对图片施加红色流年特效"))
        self.ui.treeWidget_2.topLevelItem(5).child(2).setToolTip(0, _translate("MainWindow", "对图片施加蓝色流年特效"))
        self.ui.treeWidget_2.topLevelItem(5).child(3).setToolTip(0, _translate("MainWindow", "对图片施加绿色流年特效"))


    def get_double(self):
        num1, ok = QInputDialog.getDouble(self, "double input dialog", '输入浮点数：',111,2)
        self.sigma = num1
    def get_double2(self):
        num2, ok = QInputDialog.getDouble(self, "double input dialog", '输入浮点数：',21,2)
        self.num11111 = num2

