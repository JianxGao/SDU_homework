from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.MainWindow.Main_Window_Frame import Main_Window
from matplotlib.lines import Line2D
from core.Functions import ImageFunctions
from core.edge_operation import *

class Scan_APP(QApplication):
    def __init__(self):
        super(Scan_APP,self).__init__([])
        # app主窗口
        self.main_Window = Main_Window()
        self.main_Window.show()
        self.main_Window.ui.Method_bar.hide()
        self.main_Window.ui.dockWidget_2.hide()
        self.mode = 0
        # 槽函数
        self.main_Window.ui.treeWidget_2.itemClicked['QTreeWidgetItem*', 'int'].connect(self.tree_item_clicked)
        self.main_Window.ui.treeWidget_2.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.tree_item_double_clicked)
        self.main_Window.ui.action_load_img.triggered.connect(self.load_img)
        self.main_Window.ui.action_save_img.triggered.connect(self.save_img)
        self.main_Window.ui.change_mode.clicked.connect(self.change_mode)
        self.main_Window.ui.version_control.clicked.connect(self.version_control)
        self.main_Window.ui.pushButton.clicked.connect(self.get_initial_image)
        self.history = {}
        self.main_Window.ui.text_method.clear()
        self.now_text = []
    def save_img(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(None, "保存文件", ".", "Image Files(*.jpg *.png *.tif)",)
        self.save_img_ = cv2.cvtColor(self.now_img,cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename[0], self.save_img_)
        print(filename[0])
    def get_initial_image(self):
        self.main_Window.ui.text_method.clear()
        self.now_text = []
        self.change_fig1_ax1(self.main_Window.original_img)
        self.history = {}
        self.history['img'] = [self.now_img]
        self.now_img = self.main_Window.original_img
    def version_control(self):
        if self.mode == 0:
            print('请打开专业模式')
        else:
            try:
                self.history['img'] = self.history['img'][:-1]
                self.change_fig1_ax1(self.history['img'][-1])
                self.now_img = self.history['img'][-1]
                self.now_text = self.now_text[:-1]
                self.main_Window.ui.text_method.setPlainText(''.join(self.now_text))
            except:
                print('您未操作')
    def change_mode(self):
        if self.main_Window.ui.change_mode.isChecked() == True:
        # if self.mode==0:
            self.main_Window.ui.change_mode.setChecked(1)
            self.mode = 1
            self.now_text = []
            self.main_Window.ui.text_method.clear()
            self.now_img = self.main_Window.original_img
            print('Begin X mode!')
        else:
            self.main_Window.ui.change_mode.setChecked(0)
            self.mode = 0
            self.now_img = self.main_Window.original_img
            self.main_Window.ui.text_method.clear()
            self.now_text = []
            print('End X mode!')
    def change_fig1_ax1(self, image):
        self.main_Window.fig1.ax1.cla()
        self.main_Window.fig1.ax1.imshow(image, cmap='gray')
        self.main_Window.fig1.draw()
        self.now_img = image
    def tree_item_double_clicked(self,item):
        _translate = QtCore.QCoreApplication.translate
        print(item.text(0))
        if self.mode==0:
            if "原图" == item.text(0):
                self.change_fig1_ax1(self.main_Window.original_img)
            if "增亮" == item.text(0):
                try:
                    self.change_fig1_ax1(self.brighter)
                except:
                    self.brighter = ImageFunctions(self.main_Window.original_img).brighter()
                    self.change_fig1_ax1(self.brighter)
            if "暗化" == item.text(0):
                try:
                    self.change_fig1_ax1(self.dimmer)
                except:
                    self.dimmer = ImageFunctions(self.main_Window.original_img).dimmer()
                    self.change_fig1_ax1(self.dimmer)
            if "灰度图" == item.text(0):
                try:
                    self.change_fig1_ax1(self.graystyle)
                except:
                    self.graystyle = ImageFunctions(self.main_Window.original_img).graystyle()
                    self.change_fig1_ax1(self.graystyle)
            if "黑白图" == item.text(0):
                try:
                    self.change_fig1_ax1(self.binary)
                except:
                    self.binary = ImageFunctions(self.main_Window.original_img).binary()
                    self.change_fig1_ax1(self.binary)
            if "SSR" == item.text(0):
                try:
                    self.change_fig1_ax1(self.SSR)
                except:
                    self.SSR = ImageFunctions(self.main_Window.original_img).SSR(111)
                    self.change_fig1_ax1(self.SSR)
                    self.main_Window.ui.SSR = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.SSR)
                    self.main_Window.ui.SSR.setIcon(self.get_icon_pixmap(self.SSR))
                    self.main_Window.ui.SSR.setText(_translate("MainWindow", "SSR除阴影"))
                    self.main_Window.ui.SSR.setToolTip(_translate("MainWindow", "SSR除阴影"))
                    self.main_Window.ui.SSR.triggered.connect(self.show_SSR)
            if "直方图均衡化" == item.text(0):
                try:
                    self.change_fig1_ax1(self.equalization)
                except:
                    self.equalization = ImageFunctions(self.main_Window.original_img).equalization()
                    self.change_fig1_ax1(self.equalization)
                    self.main_Window.ui.equalization = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.equalization)
                    self.main_Window.ui.equalization.setIcon(self.get_icon_pixmap(self.equalization))
                    self.main_Window.ui.equalization.setText(_translate("MainWindow", "均衡直方图"))
                    self.main_Window.ui.equalization.setToolTip(_translate("MainWindow", "均衡直方图"))
                    self.main_Window.ui.equalization.triggered.connect(self.show_equalization)
            if "Clahe" == item.text(0):
                try:
                    self.change_fig1_ax1(self.clahe)
                except:
                    self.clahe = ImageFunctions(self.main_Window.original_img).clahe()
                    self.change_fig1_ax1(self.clahe)
                    self.main_Window.ui.clahe = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.clahe)
                    self.main_Window.ui.clahe.setIcon(self.get_icon_pixmap(self.clahe))
                    self.main_Window.ui.clahe.setText(_translate("MainWindow", "Clahe"))
                    self.main_Window.ui.clahe.setToolTip(_translate("MainWindow", "Clahe"))
                    self.main_Window.ui.clahe.triggered.connect(self.show_clahe)
            if "Clahe(YUV)" == item.text(0):
                try:
                    self.change_fig1_ax1(self.claheYUV)
                except:
                    self.claheYUV = ImageFunctions(self.main_Window.original_img).claheYUV()
                    self.change_fig1_ax1(self.claheYUV)
                    self.main_Window.ui.claheYUV = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.claheYUV)
                    self.main_Window.ui.claheYUV.setIcon(self.get_icon_pixmap(self.claheYUV))
                    self.main_Window.ui.claheYUV.setText(_translate("MainWindow", "Clahe_YUV"))
                    self.main_Window.ui.claheYUV.setToolTip(_translate("MainWindow", "Clahe_YUV"))
                    self.main_Window.ui.claheYUV.triggered.connect(self.show_claheYUV)
            if "drag" == item.text(0):
                try:
                    self.change_fig1_ax1(self.drag)
                except:
                    self.drag = ImageFunctions(self.main_Window.original_img).drag()
                    self.change_fig1_ax1(self.drag)
                    self.main_Window.ui.drag = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.drag)
                    self.main_Window.ui.drag.setIcon(self.get_icon_pixmap(self.drag))
                    self.main_Window.ui.drag.setText(_translate("MainWindow", "拉伸"))
                    self.main_Window.ui.drag.setToolTip(_translate("MainWindow", "拉伸"))
                    self.main_Window.ui.drag.triggered.connect(self.show_drag)
            if "模糊" == item.text(0):
                try:
                    self.change_fig1_ax1(self.blurry)
                except:
                    self.blurry = ImageFunctions(self.main_Window.original_img).blurry()
                    self.change_fig1_ax1(self.blurry)
                    self.main_Window.ui.blurry = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.blurry)
                    self.main_Window.ui.blurry.setIcon(self.get_icon_pixmap(self.blurry))
                    self.main_Window.ui.blurry.setText(_translate("MainWindow", "模糊"))
                    self.main_Window.ui.blurry.setToolTip(_translate("MainWindow", "模糊"))
                    self.main_Window.ui.blurry.triggered.connect(self.show_blurry)
            if "平滑" == item.text(0):
                try:
                    self.change_fig1_ax1(self.smooth)
                except:
                    self.smooth = ImageFunctions(self.main_Window.original_img).smooth()
                    self.change_fig1_ax1(self.smooth)
                    self.main_Window.ui.smooth = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.smooth)
                    self.main_Window.ui.smooth.setIcon(self.get_icon_pixmap(self.smooth))
                    self.main_Window.ui.smooth.setText(_translate("MainWindow", "平滑"))
                    self.main_Window.ui.smooth.setToolTip(_translate("MainWindow", "平滑"))
                    self.main_Window.ui.smooth.triggered.connect(self.show_smooth)
            if "模板增强锐化" == item.text(0):
                try:
                    self.change_fig1_ax1(self.reinforce)
                except:
                    self.reinforce = ImageFunctions(self.main_Window.original_img).reinforce()
                    self.change_fig1_ax1(self.reinforce)
                    self.main_Window.ui.reinforce = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.reinforce)
                    self.main_Window.ui.reinforce.setIcon(self.get_icon_pixmap(self.reinforce))
                    self.main_Window.ui.reinforce.setText(_translate("MainWindow", "增强并锐化"))
                    self.main_Window.ui.reinforce.setToolTip(_translate("MainWindow", "增强并锐化"))
                    self.main_Window.ui.reinforce.triggered.connect(self.show_reinforce)
            if "USM算法增强锐化" == item.text(0):
                try:
                    self.change_fig1_ax1(self.USM)
                except:
                    self.USM = ImageFunctions(self.main_Window.original_img).USM()
                    self.change_fig1_ax1(self.USM)
                    self.main_Window.ui.USM = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.USM)
                    self.main_Window.ui.USM.setIcon(self.get_icon_pixmap(self.USM))
                    self.main_Window.ui.USM.setText(_translate("MainWindow", "增强并锐化(USM)"))
                    self.main_Window.ui.USM.setToolTip(_translate("MainWindow", "增强并锐化(USM)"))
                    self.main_Window.ui.USM.triggered.connect(self.show_USM)
            if "边缘增强" == item.text(0):
                try:
                    self.change_fig1_ax1(self.edgeRef)
                except:
                    self.edgeRef = ImageFunctions(self.main_Window.original_img).edgeRef()
                    self.change_fig1_ax1(self.edgeRef)
                    self.main_Window.ui.edgeRef = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.edgeRef)
                    self.main_Window.ui.edgeRef.setIcon(self.get_icon_pixmap(self.edgeRef))
                    self.main_Window.ui.edgeRef.setText(_translate("MainWindow", "边缘增强"))
                    self.main_Window.ui.edgeRef.setToolTip(_translate("MainWindow", "边缘增强"))
                    self.main_Window.ui.edgeRef.triggered.connect(self.show_edgeRef)
            if "边缘增强超级版" == item.text(0):
                try:
                    self.change_fig1_ax1(self.edgeRefPlus)
                except:
                    self.edgeRefPlus = ImageFunctions(self.main_Window.original_img).edgeRefPlus()
                    self.change_fig1_ax1(self.edgeRefPlus)
                    self.main_Window.ui.edgeRefPlus = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.edgeRefPlus)
                    self.main_Window.ui.edgeRefPlus.setIcon(self.get_icon_pixmap(self.edgeRefPlus))
                    self.main_Window.ui.edgeRefPlus.setText(_translate("MainWindow", "边缘增强(Beta)"))
                    self.main_Window.ui.edgeRefPlus.setToolTip(_translate("MainWindow", "边缘增强(Beta)"))
                    self.main_Window.ui.edgeRefPlus.triggered.connect(self.show_edgeRefPlus)
            if "轮廓获取" == item.text(0):
                try:
                    self.change_fig1_ax1(self.contour)
                except:
                    self.contour = ImageFunctions(self.main_Window.original_img).contour()
                    self.change_fig1_ax1(self.contour)
                    self.main_Window.ui.contour = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.contour)
                    self.main_Window.ui.contour.setIcon(self.get_icon_pixmap(self.contour))
                    self.main_Window.ui.contour.setText(_translate("MainWindow", "轮廓提取"))
                    self.main_Window.ui.contour.setToolTip(_translate("MainWindow", "轮廓提取"))
                    self.main_Window.ui.contour.triggered.connect(self.show_contour)
            if "边缘检测" == item.text(0):
                try:
                    self.change_fig1_ax1(self.edgeGet)
                except:
                    self.edgeGet = ImageFunctions(self.main_Window.original_img).edgeGet()
                    self.change_fig1_ax1(self.edgeGet)
                    self.main_Window.ui.edgeGet = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.edgeGet)
                    self.main_Window.ui.edgeGet.setIcon(self.get_icon_pixmap(self.edgeGet))
                    self.main_Window.ui.edgeGet.setText(_translate("MainWindow", "边缘检测"))
                    self.main_Window.ui.edgeGet.setToolTip(_translate("MainWindow", "边缘检测"))
                    self.main_Window.ui.edgeGet.triggered.connect(self.show_edgeGet)
            if "Otsu" == item.text(0):
                try:
                    self.change_fig1_ax1(self.Otsu)
                except:
                    self.Otsu = ImageFunctions(self.main_Window.original_img).Otsu()
                    self.change_fig1_ax1(self.Otsu)
                    self.main_Window.ui.Otsu = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.Otsu)
                    self.main_Window.ui.Otsu.setIcon(self.get_icon_pixmap(self.Otsu))
                    self.main_Window.ui.Otsu.setText(_translate("MainWindow", "Otsu"))
                    self.main_Window.ui.Otsu.setToolTip(_translate("MainWindow", "Otsu"))
                    self.main_Window.ui.Otsu.triggered.connect(self.show_Otsu)
            if "移动平均" == item.text(0):
                try:
                    self.change_fig1_ax1(self.ma)
                except:
                    self.ma = ImageFunctions(self.main_Window.original_img).ma()
                    self.change_fig1_ax1(self.ma)
                    self.main_Window.ui.ma = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.ma)
                    self.main_Window.ui.ma.setIcon(self.get_icon_pixmap(self.ma))
                    self.main_Window.ui.ma.setText(_translate("MainWindow", "移动平均"))
                    self.main_Window.ui.ma.setToolTip(_translate("MainWindow", "移动平均"))
                    self.main_Window.ui.ma.triggered.connect(self.show_ma)
            if "自适应阈值处理" == item.text(0):
                try:
                    self.change_fig1_ax1(self.adaptiveThresh)
                except:
                    self.adaptiveThresh = ImageFunctions(self.main_Window.original_img).adaptiveThresh()
                    self.change_fig1_ax1(self.adaptiveThresh)
                    self.main_Window.ui.adaptiveThresh = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.adaptiveThresh)
                    self.main_Window.ui.adaptiveThresh.setIcon(self.get_icon_pixmap(self.adaptiveThresh))
                    self.main_Window.ui.adaptiveThresh.setText(_translate("MainWindow", "自适应阈值处理"))
                    self.main_Window.ui.adaptiveThresh.setToolTip(_translate("MainWindow", "自适应阈值处理"))
                    self.main_Window.ui.adaptiveThresh.triggered.connect(self.show_adaptiveThresh)
            if "Sauvola最强二值化算法" == item.text(0):
                try:
                    self.change_fig1_ax1(self.sauvola)
                except:
                    self.sauvola = ImageFunctions(self.main_Window.original_img).sauvola()
                    self.change_fig1_ax1(self.sauvola)
                    self.main_Window.ui.sauvola = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.sauvola)
                    self.main_Window.ui.sauvola.setIcon(self.get_icon_pixmap(self.sauvola))
                    self.main_Window.ui.sauvola.setText(_translate("MainWindow", "Sauvola"))
                    self.main_Window.ui.sauvola.setToolTip(_translate("MainWindow", "Sauvola"))
                    self.main_Window.ui.sauvola.triggered.connect(self.show_sauvola)
            if "腐蚀" == item.text(0):
                try:
                    self.change_fig1_ax1(self.erode)
                except:
                    self.erode = ImageFunctions(self.main_Window.original_img).erode()
                    self.change_fig1_ax1(self.erode)
                    self.main_Window.ui.erode = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.erode)
                    self.main_Window.ui.erode.setIcon(self.get_icon_pixmap(self.erode))
                    self.main_Window.ui.erode.setText(_translate("MainWindow", "腐蚀"))
                    self.main_Window.ui.erode.setToolTip(_translate("MainWindow", "腐蚀"))
                    self.main_Window.ui.erode.triggered.connect(self.show_erode)
            if "膨胀" == item.text(0):
                try:
                    self.change_fig1_ax1(self.dilate)
                except:
                    self.dilate = ImageFunctions(self.main_Window.original_img).dilate()
                    self.change_fig1_ax1(self.dilate)
                    self.main_Window.ui.dilate = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.dilate)
                    self.main_Window.ui.dilate.setIcon(self.get_icon_pixmap(self.dilate))
                    self.main_Window.ui.dilate.setText(_translate("MainWindow", "膨胀"))
                    self.main_Window.ui.dilate.setToolTip(_translate("MainWindow", "膨胀"))
                    self.main_Window.ui.dilate.triggered.connect(self.show_dilate)
            if "开运算" == item.text(0):
                try:
                    self.change_fig1_ax1(self.opening)
                except:
                    self.opening = ImageFunctions(self.main_Window.original_img).opening()
                    self.change_fig1_ax1(self.opening)
                    self.main_Window.ui.opening = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.opening)
                    self.main_Window.ui.opening.setIcon(self.get_icon_pixmap(self.opening))
                    self.main_Window.ui.opening.setText(_translate("MainWindow", "开运算"))
                    self.main_Window.ui.opening.setToolTip(_translate("MainWindow", "开运算"))
                    self.main_Window.ui.opening.triggered.connect(self.show_opening)
            if "闭运算" == item.text(0):
                try:
                    self.change_fig1_ax1(self.closing)
                except:
                    self.closing = ImageFunctions(self.main_Window.original_img).closing()
                    self.change_fig1_ax1(self.closing)
                    self.main_Window.ui.closing = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.closing)
                    self.main_Window.ui.closing.setIcon(self.get_icon_pixmap(self.closing))
                    self.main_Window.ui.closing.setText(_translate("MainWindow", "闭运算"))
                    self.main_Window.ui.closing.setToolTip(_translate("MainWindow", "闭运算"))
                    self.main_Window.ui.closing.triggered.connect(self.show_closing)
            if "复古特效" == item.text(0):
                try:
                    self.change_fig1_ax1(self.memory)
                except:
                    self.memory = ImageFunctions(self.main_Window.original_img).memory()
                    self.change_fig1_ax1(self.memory)
                    self.main_Window.ui.memory = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.memory)
                    self.main_Window.ui.memory.setIcon(self.get_icon_pixmap(self.memory))
                    self.main_Window.ui.memory.setText(_translate("MainWindow", "复古特效"))
                    self.main_Window.ui.memory.setToolTip(_translate("MainWindow", "复古特效"))
                    self.main_Window.ui.memory.triggered.connect(self.show_memory)
            if "流年特效" == item.text(0):
                try:
                    self.change_fig1_ax1(self.yearpass)
                except:
                    self.yearpass = ImageFunctions(self.main_Window.original_img).yearpass()
                    self.change_fig1_ax1(self.yearpass)
                    self.main_Window.ui.yearpass = QtWidgets.QAction(self.main_Window)
                    self.main_Window.ui.Method_bar.addAction(self.main_Window.ui.yearpass)
                    self.main_Window.ui.yearpass.setIcon(self.get_icon_pixmap(self.yearpass))
                    self.main_Window.ui.yearpass.setText(_translate("MainWindow", "流年特效"))
                    self.main_Window.ui.yearpass.setToolTip(_translate("MainWindow", "流年特效"))
                    self.main_Window.ui.yearpass.triggered.connect(self.show_yearpass)
        if self.mode==1:
            print('xmode')
            self.now_text.append('{}\n'.format(item.text(0)))
            self.main_Window.ui.text_method.setPlainText(''.join(self.now_text))
            if "原图" == item.text(0):
                self.now_img = self.main_Window.original_img
                self.change_fig1_ax1(self.now_img)
            if "增亮" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).brighter()
                self.change_fig1_ax1(self.now_img)
            if "暗化" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).dimmer()
                self.change_fig1_ax1(self.now_img)
            if "灰度图" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).graystyle()
                self.change_fig1_ax1(self.now_img)
            if "黑白图" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).binary()
                self.change_fig1_ax1(self.now_img)
            if "SSR" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).SSR()
                self.change_fig1_ax1(self.now_img)
            if "直方图均衡化" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).equalization()
                self.change_fig1_ax1(self.now_img)
            if "Clahe" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).clahe()
                self.change_fig1_ax1(self.now_img)
            if "Clahe(YUV)" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).claheYUV()
                self.change_fig1_ax1(self.now_img)
            if "drag" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).drag()
                self.change_fig1_ax1(self.now_img)
            if "模糊" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).blurry()
                self.change_fig1_ax1(self.now_img)
            if "平滑" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).smooth()
                self.change_fig1_ax1(self.now_img)
            if "模板增强锐化" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).reinforce()
                self.change_fig1_ax1(self.now_img)
            if "USM算法增强锐化" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).USM()
                self.change_fig1_ax1(self.now_img)
            if "边缘增强" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).edgeRef()
                self.change_fig1_ax1(self.now_img)
            if "边缘增强超级版" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).edgeRefPlus()
                self.change_fig1_ax1(self.now_img)
            if "轮廓获取" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).contour()
                self.change_fig1_ax1(self.now_img)
            if "边缘检测" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).edgeGet()
                self.change_fig1_ax1(self.now_img)
            if "Otsu" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).Otsu()
                self.change_fig1_ax1(self.now_img)
            if "移动平均" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).ma()
                self.change_fig1_ax1(self.now_img)
            if "自适应阈值处理" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).adaptiveThresh()
                self.change_fig1_ax1(self.now_img)
            if "Sauvola最强二值化算法" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).sauvola()
                self.change_fig1_ax1(self.now_img)
            if "腐蚀" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).erode()
                self.change_fig1_ax1(self.now_img)
            if "膨胀" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).dilate()
                self.change_fig1_ax1(self.now_img)
            if "开运算" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).opening()
                self.change_fig1_ax1(self.now_img)
            if "闭运算" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).closing()
                self.change_fig1_ax1(self.now_img)
            if "复古特效" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).memory()
                self.change_fig1_ax1(self.now_img)
            if "流年特效" == item.text(0):
                self.now_img = ImageFunctions(self.now_img).yearpass()
                self.change_fig1_ax1(self.now_img)
            self.history['img'].append(self.now_img)
    def get_pixmap(self,image):
        if len(image.shape)==3:
            h, w, c = image.shape
            return QPixmap.fromImage(QImage(image, w, h, w * c, QImage.Format_RGB888))
        elif len(image.shape)==2:
            h, w = image.shape
            return QPixmap.fromImage(QImage(image, w, h, QImage.Format_Indexed8))
    def get_icon_pixmap(self,image):
        res_icon = QtGui.QIcon()
        res_icon.addPixmap(self.get_pixmap(image), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        return res_icon
    def load_img(self):
        print("Load img......")
        self.main_Window.ui.Method_bar.hide()
        filename, _ = QFileDialog.getOpenFileName(self.main_Window, '选择图片', 'data/', 'Image files(*.jpg *.gif *.png *.jpeg *.tif)')
        if filename == "":print('not'),self.main_Window.ui.Method_bar.show()
        else:
            print(filename)
            self.main_Window.initial_img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8),-1)
            self.main_Window.initial_filepath = filename
            self.showverts = True
            self.main_Window.initial_img = cv2.cvtColor(self.main_Window.initial_img, cv2.COLOR_BGR2RGB)
            self.now_img = self.main_Window.initial_img
            self.width, self.height = self.main_Window.initial_img.shape[:2]
            self.size = self.width * self.height
            self.offset = np.sqrt(self.size / 225)
            param = self.draw_min_rect_circle(self.main_Window.initial_img)
            if param==[]:
                x, y, w, h = 0 + self.height * 0.05, 0 + self.width * 0.05, self.height * 0.9, self.width * 0.9
            else:
                x, y, w, h = param
                if 4 * w * h < self.size:
                    x, y, w, h = 0 + self.height * 0.05, 0 + self.width * 0.05, self.height * 0.9, self.width * 0.9
            self.x = [x, x, x + w, x + w]
            self.y = [y, y + h, y + h, y]
            self.main_Window.fig1.ax1.cla()
            self.main_Window.fig1.ax1.imshow(self.main_Window.initial_img, cmap='gray')
            # self.main_Window.fig1.ax1.axis('off')
            self.line1 = Line2D(self.x, self.y,ls="-",# markersize = 20,
                                marker='o', markerfacecolor='g',animated=True,color='g')
            self.line2 = Line2D([self.x[3], self.x[0]],[self.y[3], self.y[0]],ls="-",# markersize=20,
                                marker='o', markerfacecolor='g',animated=True,color='g')
            self.main_Window.fig1.ax1.add_line(self.line1)
            self.main_Window.fig1.ax1.add_line(self.line2)
            self._ind = None
            self.draw_callback_event = self.main_Window.fig1.mpl_connect('draw_event', self.draw_callback)
            self.button_press_callback_event = self.main_Window.fig1.mpl_connect('button_press_event',self.button_press_callback)
            self.button_release_callback_event = self.main_Window.fig1.mpl_connect('button_release_event',self.button_release_callback)
            self.motion_notify_callback_event = self.main_Window.fig1.mpl_connect('motion_notify_event',self.motion_notify_callback)
            self.main_Window.fig1.draw()
            # print(dir(self.main_Window.ui.Method_bar))
            self.now_actions = self.main_Window.ui.Method_bar.actions()
            self.main_Window.ui.text_method.clear()
            self.now_text = []
            if len(self.now_actions)>=6:
                for i in range(5,len(self.now_actions)):
                    self.main_Window.ui.Method_bar.removeAction(self.now_actions[i])
                self.SSR=0
                self.equalization=0
                self.clahe=0
                self.claheYUV=0
                self.drag=0
                self.blurry=0
                self.smooth=0
                self.reinforce=0
                self.USM=0
                self.edgeRef=0
                self.edgeRefPlus=0
                self.contour=0
                self.edgeGet=0
                self.Otsu=0
                self.ma=0
                self.adaptiveThresh=0
                self.sauvola=0
                self.erode=0
                self.dilate=0
                self.opening=0
                self.closing=0
                self.memory=0
                self.yearpass=0
    def draw_callback(self, event):
        self.background = self.main_Window.fig1.copy_from_bbox(self.main_Window.fig1.ax1.bbox)
        self.main_Window.fig1.ax1.draw_artist(self.line1)
        self.main_Window.fig1.ax1.draw_artist(self.line2)
        self.main_Window.fig1.blit(self.main_Window.fig1.ax1.bbox)
    def get_ind_under_point(self, event):
        xt,yt = np.array(self.x),np.array(self.y)
        d = np.sqrt((xt-event.xdata)**2 + (yt-event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        if d[ind] >=self.offset:ind = None
        return ind
    def change(self):
        print('change')
        pts_o = np.float32(np.array([self.x,self.y]).T)
        new_height = max(pts_o[2][0]-pts_o[0][0],pts_o[3][0]-pts_o[1][0])
        new_width = max(pts_o[2][1]-pts_o[0][1],pts_o[1][1]-pts_o[3][1])
        pts_d = np.float32([[0, 0], [0, new_width], [new_height, new_width], [new_height, 0]])  # 这是变换之后的图上四个点的位置
        M = cv2.getPerspectiveTransform(pts_o, pts_d)
        self.main_Window.original_img = cv2.warpPerspective(self.main_Window.initial_img, M, (new_height, new_width))  # 最后一参数是输出dst的尺寸。可以和原来图片尺寸不一致。按需求来确定
        self.main_Window.fig1.mpl_disconnect(self.draw_callback_event)
        self.main_Window.fig1.mpl_disconnect(self.button_press_callback_event)
        self.main_Window.fig1.mpl_disconnect(self.button_release_callback_event)
        self.main_Window.fig1.mpl_disconnect(self.motion_notify_callback_event)
        self.main_Window.fig1.ax1.cla()
        self.main_Window.fig1.ax1.imshow(self.main_Window.original_img,cmap='gray')
        self.main_Window.fig1.draw()
        self.main_Window.ui.Method_bar.show()
        # Todo: 添加icon
        self.history['img'] = [self.now_img]
        self.now_img = self.main_Window.original_img
        self.main_Window.ui.original.setIcon(self.get_icon_pixmap(self.main_Window.original_img))
        self.brighter = ImageFunctions(self.main_Window.original_img).brighter()
        self.main_Window.ui.brighter.setIcon(self.get_icon_pixmap(self.brighter))
        self.dimmer = ImageFunctions(self.main_Window.original_img).reinforce()
        self.main_Window.ui.dimmer.setIcon(self.get_icon_pixmap(self.dimmer))
        self.graystyle = ImageFunctions(self.main_Window.original_img).graystyle()
        self.main_Window.ui.graystyle.setIcon(self.get_icon_pixmap(self.graystyle))
        self.binary = ImageFunctions(self.main_Window.original_img).binary()
        self.main_Window.ui.binary.setIcon(self.get_icon_pixmap(self.binary))
        self.main_Window.ui.original.triggered.connect(self.show_original)
        self.main_Window.ui.brighter.triggered.connect(self.show_brighter)
        self.main_Window.ui.dimmer.triggered.connect(self.show_dimmer)
        self.main_Window.ui.graystyle.triggered.connect(self.show_graystyle)
        self.main_Window.ui.binary.triggered.connect(self.show_binary)
    def button_press_callback(self, event):
        if not self.showverts:return
        if event.inaxes==None:return
        if event.button != 1:return
        self._ind = self.get_ind_under_point(event)
        if event.dblclick == True:self.change()
    def button_release_callback(self, event):
        if not self.showverts: return
        if event.button != 1: return
        self._ind = None
    def motion_notify_callback(self, event):
        if not self.showverts:return
        if self._ind is None:return
        if event.inaxes is None:return
        if event.button != 1:return
        x,y = event.xdata, event.ydata
        self.x[self._ind] = x
        self.y[self._ind] = y
        self.line1 = Line2D(self.x, self.y,ls="-",marker='o', markerfacecolor='g',animated=True,color='g')
        self.line2 = Line2D([self.x[0], self.x[3]],[self.y[0], self.y[3]],ls="-", marker='o', markerfacecolor='g',animated=True,color='g')
        self.main_Window.fig1.ax1.add_line(self.line1)
        self.main_Window.fig1.ax1.add_line(self.line2)
        self.main_Window.fig1.restore_region(self.background)
        self.main_Window.fig1.ax1.draw_artist(self.line1)
        self.main_Window.fig1.ax1.draw_artist(self.line2)
        self.main_Window.fig1.blit(self.main_Window.fig1.ax1.bbox)
    def draw_min_rect_circle(self, image):
        thresh = cv2.Canny(image, 128, 256)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        res_param = []
        best_size = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w * h > best_size:
                best_size = w * h
                res_param = [x, y, w, h]
        return res_param
    def tree_item_clicked(self, item):
        if item.isExpanded() == True:
            item.setExpanded(False)
        else:
            item.setExpanded(True)
    def show_original(self):
        self.change_fig1_ax1(self.main_Window.original_img)
    def show_brighter(self):
        self.change_fig1_ax1(self.brighter)
    def show_dimmer(self):
        self.change_fig1_ax1(self.dimmer)
    def show_graystyle(self):
        self.change_fig1_ax1(self.graystyle)
    def show_binary(self):
        self.change_fig1_ax1(self.binary)
    def show_SSR(self):
        self.change_fig1_ax1(self.SSR)
    def show_equalization(self):
        self.change_fig1_ax1(self.equalization)
    def show_clahe(self):
        self.change_fig1_ax1(self.clahe)
    def show_claheYUV(self):
        self.change_fig1_ax1(self.claheYUV)
    def show_drag(self):
        self.change_fig1_ax1(self.drag)
    def show_blurry(self):
        self.change_fig1_ax1(self.blurry)
    def show_smooth(self):
        self.change_fig1_ax1(self.smooth)
    def show_reinforce(self):
        self.change_fig1_ax1(self.reinforce)
    def show_USM(self):
        self.change_fig1_ax1(self.USM)
    def show_edgeRef(self):
        self.change_fig1_ax1(self.edgeRef)
    def show_edgeRefPlus(self):
        self.change_fig1_ax1(self.edgeRefPlus)
    def show_contour(self):
        self.change_fig1_ax1(self.contour)
    def show_edgeGet(self):
        self.change_fig1_ax1(self.edgeGet)
    def show_Otsu(self):
        self.change_fig1_ax1(self.Otsu)
    def show_ma(self):
        self.change_fig1_ax1(self.ma)
    def show_adaptiveThresh(self):
        self.change_fig1_ax1(self.adaptiveThresh)
    def show_sauvola(self):
        self.change_fig1_ax1(self.sauvola)
    def show_erode(self):
        self.change_fig1_ax1(self.erode)
    def show_dilate(self):
        self.change_fig1_ax1(self.dilate)
    def show_opening(self):
        self.change_fig1_ax1(self.opening)
    def show_closing(self):
        self.change_fig1_ax1(self.closing)
    def show_memory(self):
        self.change_fig1_ax1(self.memory)
    def show_yearpass(self):
        self.change_fig1_ax1(self.yearpass)
