import sys
from ui.RFIShow import RFIShow
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    demo = RFIShow()
    demo.show()
    sys.exit(app.exec_())