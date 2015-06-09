from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, backref, relationship, scoped_session
import datetime; 
import contextlib
class Database:
    def __init__(self, database_address='sqlite:///hhdb.db'):
        self.__engine = create_engine(database_address, echo=True)
        self.__session_factory = scoped_session(sessionmaker(bind=self.__engine))

    def create_tables(self):
        Base.metadata.create_all(self.__engine)
    
    @contextlib.contextmanager
    def session(self):
        session = self.__session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise

Base = declarative_base()

# class Skills(Base):
#     __tablename__='skil'
#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
#     descr = Column(Text, nullable=True)
#     id_resm = Column(Integer, ForeignKey('resm.id', ondelete='CASCADE'), nullable=False) 
    
class Positions(Base):
    __tablename__='pos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_pos = Column(Integer, nullable=False) 
    name = Column(String(255), nullable=False)
    info = Column(String(255), nullable=True)    
    e_mail = Column(String, nullable=False)
    schd = Column(String(255), nullable=False)
    trip = Column(String(255), nullable=False)  
    min_wage = Column(Integer, nullable=True)
    max_wage = Column(Integer, nullable=True)    
    experience = Column(Float, default = 0, nullable=True)
    lan = Column(String(255), nullable=True)
    educ = Column(String(255), nullable=True)
    id_empl = Column(Integer, ForeignKey('empl.id', ondelete='CASCADE'), nullable=False) 
    status = Column(Integer, nullable=True)
    
class Resume(Base):
    __tablename__='resm'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_inds = Column(Integer, ForeignKey('inds.id', ondelete='CASCADE'), nullable=False) 
    id_schd = Column(Integer, ForeignKey('schd.id'), default = 1, nullable=False) 
    id_trip = Column(Integer, ForeignKey('trip.id'), default = 1, nullable=False) 
    post = Column(String(255), nullable=True)
    min_wage = Column(Integer, nullable=True)
    max_wage = Column(Integer, nullable=True)    
    experience = Column(Float, default = 0, nullable=True)
    skills = Column(Text, nullable=True)
    id_empl = Column(Integer, ForeignKey('empl.id', ondelete='CASCADE'), nullable=False) 
    
    # skil = relationship(Skills, cascade="all, delete-orphan", passive_deletes=True)
    
class Schedule(Base):
    __tablename__='schd'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    name = Column(String(255), unique=True, nullable=False)
 
    resm = relationship(Resume)

class IsTrip(Base):
    __tablename__='trip'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    name = Column(String(255), unique=True, nullable=False)  
  
    resm = relationship(Resume)
   
class EduLang(Base):
    __tablename__='elan'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    id_lang = Column(Integer, ForeignKey('lang.id', ondelete='CASCADE'), nullable=False) 
    id_llev = Column(Integer, ForeignKey('llev.id', ondelete='CASCADE'), nullable=False) 
    id_empl = Column(Integer, ForeignKey('empl.id', ondelete='CASCADE'), nullable=False) 
    
class Education(Base):
    __tablename__='educ'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    id_univ = Column(Integer, ForeignKey('univ.id', ondelete='CASCADE'), nullable=True) 
    id_tedu = Column(Integer, ForeignKey('tedu.id'), nullable=False) 
    year_grad = Column(Date, nullable=False)
    specialty = Column(String(255), nullable=False)
    id_empl = Column(Integer, ForeignKey('empl.id', ondelete='CASCADE'), nullable=False)
           
class Empl(Base):
    __tablename__ = 'empl'
 
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    thirdname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    educ = relationship(Education, cascade="all, delete-orphan")    
    elan = relationship(EduLang, cascade="all, delete-orphan")
    resm = relationship(Resume, cascade="all, delete-orphan")
    pos = relationship(Positions, cascade="all, delete-orphan")

class TypeOfEdu(Base):
    __tablename__='tedu'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    
    educ = relationship(Education)

class LangLevel(Base):
    __tablename__='llev'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    
    elan = relationship(EduLang, cascade="all, delete-orphan", passive_deletes=True)    

class Lang(Base):
    __tablename__='lang'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    
    elan = relationship(EduLang, cascade="all, delete-orphan", passive_deletes=True)
   
class Universities(Base):
    __tablename__='univ'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    
    educ = relationship(Education, cascade="all, delete-orphan", passive_deletes=True)
        
class Industry(Base):
    __tablename__='inds'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    e_mail = Column(String(255), default = 'mbox1274-06@dev.iu7.bmstu.ru', nullable=False)
    
    resm = relationship(Resume, cascade="all, delete-orphan", passive_deletes=True)    