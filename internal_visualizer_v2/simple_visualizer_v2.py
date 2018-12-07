# Matplotlib FigureCanvas Inherited Plotting Class
# Functionality of drawing the basic graphs and process given data
# California Plug Load Research Center, 2018
# Produced by Liangze Yu

import numpy as np
from datetime import timedelta
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class Simple_Visualizer(FigureCanvas):

    def __init__(self,figure,data_dict):

        super().__init__(figure)

        # convert dict to numpy array
        self.__data_dict = data_dict

        # set up data constraints
        self.__user = None
        self.__start = None
        self.__end = None

        # cleaned data
        self.time_array = None
        self.cost_array = None

        # graph object
        self.graph = self.figure.subplots()

    def set_data(self,user,start_time,end_time):
        # define user
        self.__user = user

        # prepare datetime for clean up time datetime, 11/05/2018
        self.__start = start_time #datetime.strptime(start_time, "%m/%d/%Y")
        self.__end = end_time + timedelta(days=1) #datetime.strptime(end_time, "%m/%d/%Y")+datetime.timedelta(days=1)

        # clean data
        self.__clean_data_by_constraints()

    def __clean_data_by_constraints(self):
        # fulfill time constraints
        data = np.array(list(filter(lambda x : x[0] > self.__start and x[0] < self.__end, self.__data_dict[self.__user])))
        # get x-axis
        self.time_array = data[:,0]
        # get y-axis
        self.cost_array = data[:,1]

    def redraw(self):
        self.graph.clear()
        self.graph.plot(self.time_array,self.cost_array)
        self.graph.set_title(
            f"User: {self.__user}          Start: {self.__start.strftime('%Y-%m-%d')}          End: {self.__end.strftime('%Y-%m-%d')}" \
            , fontsize=10)
        self.graph.set_ylabel('Kilowatts')
        self.graph.figure.canvas.draw()


if '__main__' == __name__:

    from data_retriever import Data_Retriever
    # sample db,collection
    HOST = 'xxx'
    PORT = 000
    DB = 'xxx'
    COLLECTION = 'xxx'

    # sample collection keys
    USER_KEY = 'xxx'
    TIME_KEY = 'xxx'
    COST_KEY = 'xxx'

    # sample constraints
    USER_NAME = 'xxx'
    PERIOD = 'xxx'
    START = '2020-01-01 00:00'
    END = '2020-12-31 23:59'

    # data retriver
    retriever = Data_Retriever(HOST, PORT, DB, COLLECTION)
    retriever.set_retrieve_key(USER_KEY, TIME_KEY, COST_KEY)
    data_dict = retriever.get_data()

    # visualizer
    visualizer = Simple_Visualizer(data_dict)
    visualizer.set_data(USER_NAME,START,END)
    visualizer.graph()


