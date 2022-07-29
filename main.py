from PyQt5.QtWidgets import QApplication

from CMD_Login import CmdLogin

if __name__ == '__main__':
    app = QApplication([])
    form = CmdLogin()
    form.show()
    app.exec()
