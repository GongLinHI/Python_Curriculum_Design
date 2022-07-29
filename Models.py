# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Clas(Base):
    __tablename__ = 'class'

    Class = Column(String(10), primary_key=True)
    Major = Column(String(20))
    Department = Column(String(20))

    def __init__(self, Class, Major, Department):
        self.Class = Class
        self.Major = Major
        self.Department = Department

    def __repr__(self):
        return f"<Class Row Object class={self.Class},major={self.Major},department={self.Department}>"


class Course(Base):
    __tablename__ = 'course'

    Cid = Column(String(8), primary_key=True)
    Cname = Column(String(20))
    Ccredit = Column(Float(asdecimal=True))
    Cassessment = Column(String(2))

    def __init__(self, Cid, Cname, Ccredit, Cassessment):
        self.Cid = Cid
        self.Cname = Cname
        self.Ccredit = Ccredit
        self.Cassessment = Cassessment

    def __repr__(self):
        return f"<Course Row Object>"


class Teacher(Base):
    __tablename__ = 'teacher'

    Tid = Column(String(7), primary_key=True)
    Tname = Column(String(20))
    Tgender = Column(String(1))
    Tdepartment = Column(String(20))

    def __init__(self, Tid, Tname, Tgender, Tdepartment):
        self.Tid = Tid
        self.Tname = Tname
        self.Tgender = Tgender
        self.Tdepartment = Tdepartment

    def __repr__(self):
        return f"<Teacher Row Object>"


t_v_available_courses = Table(
    'v_available_courses', metadata,
    Column('Pid', String(50)),
    Column('Tname', String(20)),
    Column('Cname', String(20)),
    Column('Ptime', String(80)),
    Column('Plocation', String(80)),
    Column('Psize', Integer)
)

t_v_average_grade_class = Table(
    'v_average_grade_class', metadata,
    Column('Pid', String(50)),
    Column('Cname', String(20)),
    Column('Tname', String(20)),
    Column('Mean', Float(asdecimal=True))
)

t_v_average_grade_inv = Table(
    'v_average_grade_inv', metadata,
    Column('sid', String(10)),
    Column('Mean', Float(asdecimal=True))
)

t_v_grade = Table(
    'v_grade', metadata,
    Column('sid', String(10)),
    Column('Cname', String(20)),
    Column('Type', String(2)),
    Column('Mark', Integer),
    Column('Flag', TINYINT)
)

t_v_selected_num = Table(
    'v_selected_num', metadata,
    Column('Pid', String(50)),
    Column('Number', BigInteger, server_default=text("'0'"))
)

t_v_size_class = Table(
    'v_size_class', metadata,
    Column('Department', String(20)),
    Column('Major', String(20)),
    Column('Sclass', String(10)),
    Column('Sum', BigInteger, server_default=text("'0'")),
    Column('Boy', DECIMAL(23, 0)),
    Column('Girl', DECIMAL(23, 0))
)


class Student(Base):
    __tablename__ = 'student'

    Sid = Column(String(10), primary_key=True)
    Sname = Column(String(20))
    Sclass = Column(ForeignKey('class.Class'), index=True)
    Sgender = Column(String(1))
    Sage = Column(Integer)

    clas = relationship('Clas', backref='student')

    def __init__(self, Sid, Sname, Sclass, Sgender, Sage):
        self.Sid = Sid
        self.Sname = Sname
        self.Sclass = Sclass
        self.Sgender = Sgender
        self.Sage = Sage

    def __repr__(self):
        return f"<Student Row Object>"


class Techplan(Base):
    __tablename__ = 'techplan'

    Pid = Column(String(50), primary_key=True)
    tid = Column(ForeignKey('teacher.Tid'), index=True)
    Cid = Column(ForeignKey('course.Cid'), index=True)
    Ptime = Column(String(80))
    Plocation = Column(String(80))
    Psize = Column(Integer, comment='容量')

    course = relationship('Course', backref='techplan')
    teacher = relationship('Teacher', backref='techplan')

    def __init__(self, Pid, tid, Cid, Ptime, Plocation, Psize):
        self.Pid = Pid
        self.tid = tid
        self.Cid = Cid
        self.Ptime = Ptime
        self.Plocation = Plocation
        self.Psize = Psize

    def __repr__(self):
        return f"<Techplan Row Object>"


class Selection(Base):
    __tablename__ = 'selection'

    Sid = Column(ForeignKey('student.Sid'), primary_key=True, nullable=False)
    Pid = Column(ForeignKey('techplan.Pid'), primary_key=True, nullable=False, index=True)
    Type = Column(String(2), primary_key=True, nullable=False, comment='课程性质')
    Mark = Column(Integer, comment='成绩')
    Flag = Column(TINYINT, comment='1为补考，0为正常')

    techplan = relationship('Techplan', backref='selection')
    student = relationship('Student', backref='selection')

    def __init__(self, Sid, Pid, Type='必修', Mark=None, Flag=0):
        self.Sid = Sid
        self.Pid = Pid
        self.Type = Type
        self.Mark = Mark
        self.Flag = Flag

    def __repr__(self):
        return f"<Selection Row Object>"
