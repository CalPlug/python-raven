# QT5 Based Interval Graph Visualizer
# Take in Dictionary of Data
# Key: User, Value: (Date,Cost)
# Functionalities see README.md
# California Plug Load Research Center, 2018
# Produced by Liangze Yu

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from auto_box import ExtendedCombo
from data_retriever import Data_Retriever
from simple_visualizer_v2 import Simple_Visualizer
from datetime import datetime
from datetime import timedelta
import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.dates import num2date,date2num

class Ui_Visualizer_Internal(object):

    def __init__(self,users, data_dict):
        # static fields
        self.__users = users
        self.__data_dict = data_dict

        # dynamic fields
        self.__current_user = self.__users[0]
        self.__start_bound = min(self.__data_dict[self.__current_user])[0]
        self.__end_bound = max(self.__data_dict[self.__current_user])[0]

    def setupUi(self, Visualizer_Internal):
        Visualizer_Internal.setObjectName("Visualizer_Internal")
        Visualizer_Internal.resize(1037, 615)
        self.Visualizer_Internal = Visualizer_Internal
        self.centralWidget = QtWidgets.QWidget(Visualizer_Internal)
        self.centralWidget.setObjectName("centralWidget")

        # apply reset
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralWidget)
        self.buttonBox.setGeometry(QtCore.QRect(820, 400, 77, 66))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Draw")
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        # test Apply and Reset
        self.buttonBox.clicked.connect(self.handle_button_click)

        # graphic view layout
        self.widgetg = QtWidgets.QWidget(self.centralWidget)
        self.widgetg.setGeometry(QtCore.QRect(0, 0, 1041, 340))
        self.widgetg.setObjectName("widget")
        self.graphicsView = QtWidgets.QVBoxLayout(self.widgetg)
        self.graphicsView.setObjectName("graphicsView")
        # graph construction
        self.static_canvas = Simple_Visualizer(Figure(),self.__data_dict)
        self.graphicsView.addWidget(self.static_canvas)
        self.static_canvas.set_data(self.__current_user,self.__start_bound,self.__end_bound)
        self.static_canvas.graph.figure.canvas.callbacks.connect('motion_notify_event', self.mouse_movement)
        self.static_canvas.redraw()
        Visualizer_Internal.addToolBar(NavigationToolbar(self.static_canvas, Visualizer_Internal))
        # set up tracing dot
        self.dot = None

        #horizontal QHBoxLayout layout
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(60, 320, 521, 101))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # user line
        model = QtGui.QStandardItemModel()
        for i, word in enumerate(self.__users):
            item = QtGui.QStandardItem(word)
            model.setItem(i, 0, item)
        self.combo = ExtendedCombo()
        self.combo.setModel(model)
        self.combo.setModelColumn(0)
        self.horizontalLayout.addWidget(self.combo)
        # confirm user
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        # testing confirm user
        self.pushButton.clicked.connect(self.change_user)

        # horizontal QHBoxLayout layout2
        self.widget3 = QtWidgets.QWidget(self.centralWidget)
        self.widget3.setGeometry(QtCore.QRect(70, 410, 600, 200))
        self.widget3.setObjectName("widget")
        #self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.widget3)
        # tracing info
        self.label_3 = QtWidgets.QLabel(self.widget3)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label")

        #vertical QVBoxLayout layout
        self.widget1 = QtWidgets.QWidget(self.centralWidget)
        self.widget1.setGeometry(QtCore.QRect(650, 340, 130, 171))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        # start
        self.label = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        # start date
        self.dateEdit_2 = QtWidgets.QDateEdit(self.widget1)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dateEdit_2.setDisplayFormat("MM/dd/yyyy")
        self.dateEdit_2.setDateTime(self.__start_bound)
        self.dateEdit_2.setMinimumDateTime(self.__start_bound)
        # end
        self.verticalLayout.addWidget(self.dateEdit_2)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        # end date
        self.dateEdit = QtWidgets.QDateEdit(self.widget1)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDisplayFormat("MM/dd/yyyy")
        self.dateEdit.setDateTime(self.__end_bound)
        self.dateEdit.setMaximumDateTime(self.__end_bound)
        self.verticalLayout.addWidget(self.dateEdit)

        # tool bars
        Visualizer_Internal.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(Visualizer_Internal)
        self.mainToolBar.setObjectName("mainToolBar")
        Visualizer_Internal.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(Visualizer_Internal)
        self.statusBar.setObjectName("statusBar")
        Visualizer_Internal.setStatusBar(self.statusBar)

        self.retranslateUi(Visualizer_Internal)
        QtCore.QMetaObject.connectSlotsByName(Visualizer_Internal)

        # set resize function
        Visualizer_Internal.resize_function = self.resize

    def retranslateUi(self, Visualizer_Internal):
        _translate = QtCore.QCoreApplication.translate
        Visualizer_Internal.setWindowTitle(_translate("Visualizer_Internal", "Visualizer_Internal"))
        self.pushButton.setText(_translate("Visualizer_Internal", "Change User"))
        self.label.setText(_translate("Visualizer_Internal", "Start Date\nM/D/Y"))
        self.label_2.setText(_translate("Visualizer_Internal", "End Date\nM/D/Y"))
        self.label_3.setText(_translate("Visualizer_Internal", "Cost: None"+' '*100+'\n\nDate: None'+' '*100))

    def change_user(self):
        # set current user
        self.__current_user = self.combo.currentText()

        #set dates
        self.__start_bound = min(self.__data_dict[self.__current_user])[0]
        self.__end_bound = max(self.__data_dict[self.__current_user])[0]

        # Weird Bug need to set time twice
        self.set_time()
        self.set_time()

    def set_time(self):
        #start date
        self.dateEdit_2.setDateTime(self.__start_bound)
        self.dateEdit_2.setMinimumDateTime(self.__start_bound)

        #end date
        self.dateEdit.setDateTime(self.__end_bound)
        self.dateEdit.setMaximumDateTime(self.__end_bound)

        # reset canvas
        self.dot = None
        self.static_canvas.set_data(self.__current_user, self.__start_bound, self.__end_bound)
        self.static_canvas.redraw()

    def handle_button_click(self, button):
        sb = self.buttonBox.standardButton(button)
        if sb == QtWidgets.QDialogButtonBox.Apply:
            start = datetime.strptime(self.dateEdit_2.text(), "%m/%d/%Y")
            end = datetime.strptime(self.dateEdit.text(), "%m/%d/%Y")

            if start > self.__end_bound:
                start = self.__end_bound - timedelta(days=1)
            if end < self.__start_bound:
                end = self.__start_bound + timedelta(days=1)
            if start > end:
                end = start + timedelta(days=1)

            self.dateEdit_2.setDateTime(start)
            self.dateEdit.setDateTime(end)

            # reset canvas
            self.dot = None
            self.static_canvas.set_data(self.__current_user,start,end)
            self.static_canvas.redraw()
            print(f'Apply Clicked')

        elif sb == QtWidgets.QDialogButtonBox.Reset:
            self.dateEdit_2.setDateTime(self.__start_bound)
            self.dateEdit.setDateTime(self.__end_bound)

            #reset canvas
            self.dot = None
            self.static_canvas.set_data(self.__current_user, self.__start_bound, self.__end_bound)
            self.static_canvas.redraw()
            print('Reset Clicked')

    def resize(self):
        # manually initial
        original_width = 1037
        original_height = 615

        # updated initial
        window_width = self.Visualizer_Internal.geometry().width()
        window_height = self.Visualizer_Internal.geometry().height()

        # update ratio
        width_ratio = window_width/original_width
        height_ratio = window_height/original_height

        # update all widgets
        self.buttonBox.setGeometry(QtCore.QRect(820*width_ratio, 400*height_ratio, 77*width_ratio, 66*height_ratio))
        self.widgetg.setGeometry(QtCore.QRect(0, 0, 1041*width_ratio, 340*height_ratio))
        self.widget.setGeometry(QtCore.QRect(60*width_ratio, 320*height_ratio, 521*width_ratio, 101*height_ratio))
        self.widget1.setGeometry(QtCore.QRect(650*width_ratio, 340*height_ratio, 130*width_ratio, 171*height_ratio))
        self.widget3.setGeometry(QtCore.QRect(70*width_ratio, 410*height_ratio, 600*width_ratio, 200*height_ratio))

    def mouse_movement(self,event):
        if not event.inaxes:
            return

        # naive and aware
        x, y = num2date(event.xdata).replace(tzinfo=None), event.ydata
        x_list = self.static_canvas.time_array
        y_list = self.static_canvas.cost_array

        # trace the position of x
        indx = np.searchsorted(x_list, [x])[0]
        if indx >= len(x_list):
            return
        x = x_list[indx]
        y = y_list[indx]

        # reset ablines
        if len(self.static_canvas.graph.lines) != 1:
            self.static_canvas.graph.lines[-1].remove()
            self.static_canvas.graph.lines[-1].remove()
        self.static_canvas.graph.axvline(x, c="red", linewidth=1, zorder=0)
        self.static_canvas.graph.axhline(y, c="red", linewidth=1,zorder=0)

        # reset tracing dot
        if self.dot != None:
            self.dot.remove()
        self.dot = self.static_canvas.graph.scatter(x,y,c='red')
        self.static_canvas.graph.figure.canvas.draw()

        # update label
        self.label_3.setText(QtCore.QCoreApplication.translate("Visualizer_Internal", f"Cost: {y}\n\nDate: {x.strftime('%Y-%m-%d %H:%M')}"))

class Resizeable_MainWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    resize_function = None
    def resizeEvent(self, event):
        if self.resize_function != None:
            self.resize_function()
        QtWidgets.QMainWindow.resizeEvent(self, event)

if __name__ == "__main__":

    # Setup
    HOST = 'xxx'
    PORT = 0000
    DB = 'xxx'
    COLLECTION = 'xxx'
    USER_KEY = 'xxx'
    TIME_KEY = 'xxx'
    COST_KEY = 'xxx'

    # retriver object
    retriever = Data_Retriever(HOST, PORT, DB, COLLECTION)
    retriever.set_retrieve_key(USER_KEY, TIME_KEY, COST_KEY)
    # main window
    app = QtWidgets.QApplication(sys.argv)
    Visualizer_Internal = Resizeable_MainWindow()
    ui = Ui_Visualizer_Internal(retriever.get_users(),retriever.get_data())
    ui.setupUi(Visualizer_Internal)
    Visualizer_Internal.show()
    sys.exit(app.exec_())

