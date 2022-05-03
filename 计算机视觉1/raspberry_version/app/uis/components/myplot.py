from uis.components.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
matplotlib.use('Qt5Agg')

class Myplot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=2, height=3, dpi=100):
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


class static_fig(Myplot):
    def __init__(self, *args, **kwargs):
        Myplot.__init__(self, *args, **kwargs)

