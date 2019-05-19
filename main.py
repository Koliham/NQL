import os

from PyQt5 import QtWidgets
from nldlgui import Ui_MainWindow
import sys


from StreamTextEdit import StreamTextEdit
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "D:/Programme/Anaconda3/Library/plugins/platforms"

def converthandler(self):
    print("handling convert button")
    processInputNL("test")

def processInputNL(input):
    print("processing input"+input)

def neuefunc():
    print("neu")

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.txtNL = StreamTextEdit(self.ui.centralwidget)
        self.ui.btnConvert.clicked.connect(lambda x: processInputNL(self.ui.txtNL.toPlainText()))
        self.ui.txtNL.outputfeld = self.ui.txtResultDSL
        self.ui.txtNL.setSuggestlist(self.ui.listvorschlaege)
        self.ui.txtNL.startBackgroundThread()
        # self.ui.txtNL.keyReleaseEvent.connect(lambda x: processInputNL(self.ui.txtNL.toPlainText()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()