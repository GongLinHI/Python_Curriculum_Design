from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from GUI.Login import Ui_Form_login
from SessMaker import db_connector
from Models import Student
from CMD_MainWIndow import CmdMainWindow


class CmdLogin(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form_login()
        self.ui.setupUi(self)
        self.MW = CmdMainWindow()

        # 控件关联
        self.ui.pushButton_login.clicked.connect(self.method_ok)
        self.ui.pushButton_cancel.clicked.connect(self.method_cancel)

    def method_ok(self):
        db_acc = None
        acc = self.ui.lineEdit_Account.text()
        passwd = self.ui.lineEdit_Password.text()
        SessMaker = db_connector()
        sess = SessMaker()
        try:
            db_acc = sess.query(Student).filter(Student.Sid == acc).first()
        except Exception as err:
            print(err)
        finally:
            sess.close()

        if db_acc is None:
            QMessageBox.information(self, '错误', "用户名或密码错误", QMessageBox.Retry)
        else:
            valid_passwd = db_acc.Sname
            if valid_passwd == passwd:
                self.MW.show()
                self.close()
            else:
                QMessageBox.information(self, '错误', "用户名或密码错误", QMessageBox.Retry)

    def method_cancel(self):
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    form = CmdLogin()
    form.show()
    app.exec()
