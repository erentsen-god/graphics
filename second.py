import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QTableWidgetItem, QWidget
from MainWindow import Ui_MainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import numpy as np
import numexpr as ne
import pylab


def plot_single_empty_graph():
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 7), dpi=85,
                             facecolor='white', frameon=True, edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    axes.set_title('Графики линейных функций', fontsize=10)
    axes.set_xlabel('X', fontsize=8)
    axes.set_ylabel('Y', fontsize=8)
    return fig, axes


def plot_custom_function(axes=None, function=None,
                         legend=None, name=None,
                         limits=None, type='y=f(x)'):
    left_limit = limits[0]
    right_limit = limits[1]
    step = (max(limits) - min(limits))/1000
    if type == 'y=f(x)':
        legend.append('y='+str(function))
        x_vals = np.arange(left_limit, right_limit, step)
        y = []
        function = function.replace('^', '**').strip()
        function = function.replace('X', 'x')
        for x in x_vals:
            y.append(ne.evaluate(function))
        plot_instance, = axes.plot(x_vals, y, '-', lw=1)
        axes.set_xlim(left_limit, right_limit)
        axes.set_ylim(left_limit, right_limit)
        axes.legend(legend, loc='best', fontsize=8)
    return plot_instance


class MainWindow(QMainWindow, Ui_MainWindow):
    graph_legend = []

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.fig, self.axes = plot_single_empty_graph()

        self.companovka_for_mpl = QVBoxLayout(self.widget)
        self.canavas = MyMplCanvas(self.fig)
        self.companovka_for_mpl.addWidget(self.canavas)
        self.toolbar = NavigationToolbar2QT(self.canavas, self)
        self.companovka_for_mpl.addWidget(self.toolbar)

        self.pushButton.clicked.connect(self.plot_function)



    def plot_function(self):
        function = self.input_function_line.toPlainText()
        function_instance = plot_custom_function(axes=self.axes,
                                                 function=function,
                                                 legend=self.graph_legend,
                                                 limits=[int(self.ox_0.displayText()), int(self.ox_2.displayText())])
        self.fig.canvas.draw()
        self.plainTextEdit.appendPlainText(self.input_function_line.toPlainText())



class MyMplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig):
        self.fig = fig
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


def main_application():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    main_application()