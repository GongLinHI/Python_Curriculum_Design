import sqlalchemy
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidgetItem, QFileDialog
from GUI.MainWindow import Ui_MainWindow
from SessMaker import db_connector, my_engine
from Models import *
import pandas as pd


class CmdMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.SessMaker = db_connector()
        self.sess = self.SessMaker()
        # 控件关联

        self.ui.pushButton_Sid.clicked.connect(self.query_info_by_sid)
        self.ui.pushButton_Sname.clicked.connect(self.query_info_by_sname)
        self.ui.pushButton_add.clicked.connect(self.insert_info)
        self.ui.pushButton_submit.clicked.connect(self.update_info)

        self.ui.pushButton_select.clicked.connect(self.query_course)
        self.ui.pushButton_commit.clicked.connect(self.commit_course)

        self.ui.pushButton_select_2.clicked.connect(self.query_score)

        self.ui.pushButton_browse.clicked.connect(self.browse)
        self.ui.pushButton_import.clicked.connect(self.Import)

    # 按照学号查找信息 pass
    def query_info_by_sid(self):
        target_sid = self.ui.lineEdit_1_sid.text()
        try:
            resp = self.sess.query(Student).filter(Student.Sid == target_sid).first()
            if resp is None:
                QMessageBox.information(self, 'information', "学号不正确", QMessageBox.Retry)
            else:
                self.display_info(resp)
        except Exception as err:
            print(err)

    # 按照姓名查找信息 pass
    def query_info_by_sname(self):
        target_sname = self.ui.lineEdit_2_sname.text()
        try:
            resp = self.sess.query(Student).filter(Student.Sname == target_sname).first()
            if resp is None:
                QMessageBox.information(self, 'information', "姓名不正确", QMessageBox.Retry)
            else:
                self.display_info(resp)
        except Exception as err:
            print(err)

    # 显示个人信息 pass
    def display_info(self, row: sqlalchemy.engine.row.Row):
        sid = row.Sid
        sname = row.Sname
        sclass = row.Sclass
        sgender = row.Sgender
        sage = row.Sage
        sdept = row.clas.Department
        self.ui.lineEdit_1_sid.setText(sid)
        self.ui.lineEdit_2_sname.setText(sname)
        self.ui.lineEdit_3_ssex.setText(sgender)
        self.ui.lineEdit_4_sage.setText(str(sage))
        self.ui.lineEdit_5_sdept.setText(sdept)
        self.ui.lineEdit_6_sclass.setText(sclass)

    # 添加个人信息 pass
    def insert_info(self):

        # 获取从用户的输入
        sid = self.ui.lineEdit_1_sid.text()
        sname = self.ui.lineEdit_2_sname.text()
        sclass = self.ui.lineEdit_6_sclass.text()
        sgender = self.ui.lineEdit_3_ssex.text()
        sage = self.ui.lineEdit_4_sage.text()
        # sdept = self.ui.lineEdit_5_sdept.text()

        # 判断是否合法
        resp = self.sess.query(Student).filter(Student.Sid == sid).first()
        if resp is not None:  # 信息已经存在
            QMessageBox.information(self, 'information', '此人信息已经存在，无需添加', QMessageBox.Ok)
            return

        resp2 = self.sess.query(Clas).all()
        clas_list = []
        for row in resp2:
            clas_list.append(row.Class)
        if sclass not in clas_list:  # 信息非法
            QMessageBox.warning(self, '错误', '信息非法，无法添加', QMessageBox.Retry)
            return

        # 插入信息
        val = Student(Sid=sid, Sname=sname, Sgender=sgender, Sclass=sclass, Sage=sage)
        try:
            self.sess.add(val)
            self.sess.commit()
        except Exception as err:
            QMessageBox.warning(self, '错误', '添加失败', QMessageBox.Retry)
            print(err)
        else:
            QMessageBox.information(self, 'information', "添加成功", QMessageBox.Ok)

    # 更新个人信息
    def update_info(self):

        # 获取从用户的输入
        sid = self.ui.lineEdit_1_sid.text()
        sname = self.ui.lineEdit_2_sname.text()
        sclass = self.ui.lineEdit_6_sclass.text()
        sgender = self.ui.lineEdit_3_ssex.text()
        sage = self.ui.lineEdit_4_sage.text()
        sdept = self.ui.lineEdit_5_sdept.text()

        print(sid, sname, sclass, sgender, sage, sdept)
        flag = True
        if sid is None:
            flag = False
        elif sname is None:
            flag = False
        elif sclass is None:
            flag = False
        elif sgender is None:
            flag = False
        elif sage is None:
            flag = False
        elif sdept is None:
            flag = False

        if flag is False:
            QMessageBox.information(self, 'information', "请先查询在更改信息", QMessageBox.Ok)
            return

        resp = self.sess.query(Student).filter(Student.Sid == sid).first()
        if resp.clas.Department != sdept:
            QMessageBox.Warning(self, '警告', '不允许更改此项', QMessageBox.Ok)
            return
        if sname != resp.Sname:
            self.sess.query(Student).filter(Student.Sid == sid).update({'Sname': sname})
        elif sclass != resp.Sclass:
            self.sess.query(Student).filter(Student.Sid == sid).update({'Sclass': sclass})
        elif sgender != resp.Sgender:
            self.sess.query(Student).filter(Student.Sid == sid).update({'Sgender': sgender})
        elif sage != resp.Sage:
            self.sess.query(Student).filter(Student.Sid == sid).update({'Sage': sage})
        self.sess.commit()
        QMessageBox.information(self, 'information', '提交更改成功', QMessageBox.Ok)

    # 查询可选课程
    def query_course(self):
        resp = []
        index = self.ui.comboBox.currentIndex()
        text = self.ui.lineEdit_val.text()
        if index == 0:  # index:0 请选择
            QMessageBox.information(self, 'information', '请选择查询条件', QMessageBox.Ok)
            return
        elif index == 1:  # index:1 按课程名称
            resp = self.sess.query(t_v_available_courses).filter(
                t_v_available_courses.c.Cname.like('%' + str(text) + '%')).all()
        elif index == 2:  # index:2 按教师姓名
            resp = self.sess.query(t_v_available_courses).filter(
                t_v_available_courses.c.Tname.like('%' + str(text) + '%')).all()
        if len(resp) == 0:
            QMessageBox.information(self, 'information', '没有找到相应的课程', QMessageBox.Retry)
            return
        else:
            df = pd.DataFrame(resp)
            table = self.ui.tableWidget_course
            self.display_dynamic_form(df, table)

    # 动态表格
    def display_dynamic_form(self, df, target_obj):

        # horizontalHeader().setVisible
        # .verticalHeader().setVisible
        input_table_rows = df.shape[0]
        input_table_colunms = df.shape[1]
        input_table_header = df.columns.values.tolist()
        target_obj.setColumnCount(input_table_colunms)
        target_obj.setRowCount(input_table_rows)
        target_obj.setHorizontalHeaderLabels(input_table_header)
        # print(input_table_header)
        for i in range(input_table_rows):
            for j in range(input_table_colunms):
                new_item = QTableWidgetItem(str(df.iat[i, j]))
                target_obj.setItem(i, j, new_item)

    # 选课 pass
    def commit_course(self):
        sid = self.ui.lineEdit_Sid.text()
        pid = self.ui.lineEdit_pid.text()
        if sid and pid:
            resp1 = self.sess.query(Student).filter(Student.Sid == sid).first()
            resp2 = self.sess.query(Techplan).filter(Techplan.Pid == pid).first()
            resp3 = self.sess.query(Selection).filter(Selection.Sid == sid, Selection.Pid == pid).first()
            if resp1 and resp2:
                if resp3:
                    QMessageBox.information(self, 'information', '你已经选过了', QMessageBox.Ok)
                    return
                else:
                    try:
                        val = Selection(Sid=sid, Pid=pid, Type='必修', Flag=0)
                        self.sess.add(val)
                        self.sess.commit()
                    except Exception as err:
                        print(err)
                    else:
                        QMessageBox.information(self, 'information', '选课成功', QMessageBox.Ok)
                    return
        else:
            QMessageBox.information(self, 'information', '输入有误', QMessageBox.Retry)

    # 教学班成绩 pass
    def query_score(self):
        resp = []
        index = self.ui.comboBox_2.currentIndex()
        text = self.ui.lineEdit_val_2.text()
        if index == 0 and text != 'all':  # index:0 请选择
            QMessageBox.information(self, 'information', '请选择查询条件', QMessageBox.Ok)
            return
        elif index == 1:
            resp = self.sess.query(t_v_average_grade_class).filter(
                t_v_average_grade_class.c.Cname.like('%' + str(text) + '%')).all()
        elif index == 2:
            resp = self.sess.query(t_v_average_grade_class).filter(
                t_v_average_grade_class.c.Tname.like('%' + str(text) + '%')).all()
        if text == 'all':
            resp = self.sess.query(t_v_average_grade_class).all()

        if len(resp) == 0:
            QMessageBox.information(self, 'information', '没有找到相应的教学班', QMessageBox.Retry)
            return
        else:
            df = pd.DataFrame(resp)
            table = self.ui.tableWidget_2
            self.display_dynamic_form(df, table)

    # 浏览
    def browse(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取单个源文件",
                                                            "D:\Code\Python_Curriculum_Design",
                                                            "Microsoft Excel File(*.xlsx);;Microsoft Excel File(*.xls);;CSV File(*.csv);;Text Files (*.txt);;All Files (*)")
        # Text Files (*.txt);;,*.xls
        self.ui.lineEdit_path.setText(get_filename_path)

    # 导入
    def Import(self):
        path = self.ui.lineEdit_path.text()
        if path == '':  # 无内容返回空字符串
            QMessageBox.information(self, 'information', '没有选择文件', QMessageBox.Ok)
            return
        # print(path)
        file_extension = path.split('.')[-1]
        file_name = path.split('/')[-1]
        index = self.ui.listWidget.currentIndex()
        text = index.data()
        # print(text)
        succ_num = 0
        if file_extension == 'xls' or file_extension == 'xlsx':
            data_df = pd.read_excel(io=path)
        elif file_extension == 'csv' or file_extension == 'txt':
            data_df = pd.read_csv(path)
        else:
            QMessageBox.information(self, 'information', "不支持导入", QMessageBox.Ok)
            return
        if text is None:
            QMessageBox.information(self, 'information', "请选择目标表格", QMessageBox.Retry)
            return
        try:
            if text == "学生信息":
                data_df.columns = ['Sid', 'Sname', 'Sclass', 'Sgender', 'Sage']
                succ_num = data_df.to_sql(name='student', con=my_engine, if_exists='append', index=False)
            elif text == "教师信息":
                data_df.columns = ['Tid', 'Tname', 'Tgender', 'Tdepartment']
                succ_num = data_df.to_sql(name='teacher', con=my_engine, if_exists='append', index=False)
            elif text == "班级信息":
                data_df.columns = ['Class', 'Major', 'Department']
                succ_num = data_df.to_sql(name='class', con=my_engine, if_exists='append', index=False)
            elif text == "选课信息":
                data_df.columns = ['Sid', 'Pid', 'Type', 'Mark', 'Flag']
                succ_num = data_df.to_sql(name='selection', con=my_engine, if_exists='append', index=False)
            elif text == "课程信息":
                data_df.columns = ['Cid', 'Cname', 'Ccredit', 'Cassessment']
                succ_num = data_df.to_sql(name='course', con=my_engine, if_exists='append', index=False)
            elif text == "教学计划信息":
                data_df.columns = ['Pid', 'tid', 'Cid', 'Ptime', 'Plocation', 'Psize']
                succ_num = data_df.to_sql(name='techplan', con=my_engine, if_exists='append', index=False)
        except Exception as err:
            print(err)
            QMessageBox.information(self, 'information', "导入失败", QMessageBox.Retry)
        else:
            QMessageBox.information(self, 'information', f"导入成功,共{succ_num}条数据", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication([])
    window = CmdMainWindow()
    window.show()
    app.exec()
