from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

from GUI.test import Ui_Form


class Test_Command(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 控件关联
        self.ui.Button_OK.clicked.connect(self.method_ok)
        self.ui.Button_Cancel.clicked.connect(self.method_cancel)

    def method_ok(self):
        val_1 = self.ui.lineEdit_1.text()
        val_2 = self.ui.lineEdit_2.text()

    def method_cancel(self):
        self.close()


app = QApplication([])
form = Test_Command()
form.show()
app.exec()
