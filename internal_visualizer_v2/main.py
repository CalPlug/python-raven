# QT5 Based Interval Graph Visualizer
# Take in Dictionary of Data
# Key: User, Value: (Date,Cost)
# Functionalities see README.md
# California Plug Load Research Center, 2018
# Produced by Liangze Yu

import sys
from PyQt5 import QtWidgets
from data_retriever import Data_Retriever
from visualizer_internal_v2 import Ui_Visualizer_Internal, Resizeable_MainWindow


if __name__ == '__main__':

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