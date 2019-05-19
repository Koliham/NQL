
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QKeySequence

from nldslfuncs import nldslparser
from importlib import reload
import sys
import traceback
import threading


class UpdateThread(QtCore.QThread):
    inputtext : str = ""
    inputfield : QtWidgets.QTextEdit

    data_downloaded = QtCore.pyqtSignal(object)
    result = ""
    refreshcounter = 0
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while(False):
            self.msleep(500)
            print("refreshing " + str(self.refreshcounter))
            self.refreshcounter += 1
            nldslfuncs = reload(nldslparser)
            result = nldslparser.nldslparse(self.inputfield.toPlainText())
            self.data_downloaded.emit(result)

class StreamTextEdit(QtWidgets.QTextEdit):

    lastselectedIndex : int = 0 # shows the first entry as default
    refreshcounter : int = 0
    outputfeld : QtWidgets.QTextEdit
    suggestlist: QtWidgets.QListWidget
    currentsuggestions = []
    currentinput :str = ""
    refreshthread : UpdateThread
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Expanding, PyQt5.QtWidgets.QSizePolicy.Expanding)
        self.show()


    def setSuggestlist(self,liste : QtWidgets.QListWidget):
        self.suggestlist = liste
        self.suggestlist.itemSelectionChanged.connect(self.showSelectedSuggestion)



    def showSelectedSuggestion(self):
        #read the current selected index. If there is one, change the last selected index
        if len(self.suggestlist.selectedIndexes()) != 0:
            self.lastselectedIndex = self.suggestlist.selectedIndexes()[0].row()
        try:
            #it can happen, that the last selected doesnt exist anymore:
            if self.lastselectedIndex +1 > len(self.currentsuggestions):
                self.lastselectedIndex = len(self.currentsuggestions) -1
            self.outputfeld.setText(str(self.currentsuggestions[self.lastselectedIndex]["result"]))
            # self.outputfeld.setText(self.outputfeld.toPlainText() + " " + str(self.refreshcounter))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exc(file=sys.stdout)
            self.outputfeld.setText(traceback.format_exc())


    def startBackgroundThread(self):
        self.refreshthread = UpdateThread()
        self.refreshthread.inputfield = self
        self.refreshthread.data_downloaded.connect(self.refreshViews)
        self.refreshthread.start()
        # self.refreshthread = threading.Thread(target=self.reloadData)
        # self.refreshthread.start()


    def reloadData(self):
        # print("refreshing " + str(self.refreshcounter))
        self.refreshcounter += 1
        nldslfuncs = reload(nldslparser)
        self.currentsuggestions = nldslparser.nldslparse(self.toPlainText())


    def refreshViews(self,daten=None):
        if daten is not None:
            self.currentsuggestions = daten
        self.suggestlist.clear()
        for eintrag in self.currentsuggestions:
            self.suggestlist.addItem(eintrag["suggestion"] + " " + str(eintrag["chance"]))
        self.showSelectedSuggestion()  # default is index 0

    def refreshPage(self):
        #refresh
        self.reloadData()
        self.refreshViews()


    def keyReleaseEvent(self, event):
        self.refreshPage()

        if event.key() == 16777220: #PyQt5.QtCore.Qt.Key_Enter:
            print("enter gedrück")
        #     self.get_and_send()
        # else:
        super().keyReleaseEvent(event)