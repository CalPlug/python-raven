from raven import Raven
from SQLiteHelper import SQLiteHelper
import xml.etree.ElementTree as ET

from time import sleep
import tkinter
import time
import threading
import random
from collections import deque


STARTTIME = 946684800

def raven_to_unix_time(t:int):
    return t+STARTTIME

def unix_to_raven_time(t:int):
    return t-STARTTIME


class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        self.console = tkinter.Text(master)
        
        self.strvar = tkinter.StringVar()

        self.entry_box = tkinter.Entry(master, textvariable = self.strvar)
        entry_box.pack()    
        
        self.button = tktinter.Button(master, self.onButtonPress)

    def 

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        if len(self.queue) > 0:
            self.console.delete("1.0",tkinter.END)
        while len(self.queue):
            try:
                msg = self.queue.popleft()
                self.console.insert("1.0",msg+"\n")
            except:
                pass



class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master
        self.raven = Raven()
        # Create the queue
        self.queue = deque()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        db = SQLiteHelper('energy_channel.db')
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            GET_DEMAND = {'Name':'get_instantaneous_demand'}
            self.raven.write(GET_DEMAND)
            # Sleeping the device for a little just in case.
            sleep(.1)
            response = self.raven.read()
            attributes = response.getchildren()
            attribute_list = [3,4,5,2]
            data = tuple(int(attributes[i].text, 16) for i in attribute_list)
            db.insert_data(data)
            for i in db.get_last_n_rows(5):
                self.queue.append("DEMAND : {} TIME : {}".format(i[1] * i[2]/i[3], i[4]))
            sleep(7)

            time.sleep(1)

    def endApplication(self):
        self.running = 0

if __name__ == '__main__':
    root = tkinter.Tk()
    client = ThreadedClient(root)
    root.mainloop()
##    s = SQLiteHelper('energy_channel.db')
##    r = Raven()
##    GET_DEMAND = {'Name':'get_instantaneous_demand'}
##    if not r.checkRaven():
##        print('No RaveN found. Please reinsert the device and run this script again')
##    else:
##        while True:
##            r.write(GET_DEMAND)
##            # Sleeping the device for a little just in case.
##            sleep(.1)
##            response = r.read()
##            attributes = response.getchildren()
##            attribute_list = [3,4,5,2]
##            data = tuple(int(attributes[i].text, 16) for i in attribute_list)
##            s.insert_data(data)
##            for i in s.get_last_n_rows(5):
##                print(i)
##            sleep(7)
##            print("--------New Cycle---------")
