from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, backref, relationship, scoped_session
import datetime; 
import contextlib

class Database:
    def __init__(self, database_address='sqlite:///iadb.db'):
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

class RelationCvPos(Base):
    __tablename__='relationCvPos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_pos = Column(Integer, ForeignKey('pos.id', ondelete='CASCADE'), nullable=False)
    id_resm = Column(Integer, ForeignKey('resm.id', ondelete='CASCADE'), nullable=False) 
    status = Column(Integer, nullable=True)
    
class EduLang(Base):
    __tablename__='elan'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    id_lang = Column(Integer, ForeignKey('lang.id', ondelete='CASCADE'), nullable=True) 
    id_llev = Column(Integer, ForeignKey('llev.id', ondelete='CASCADE'), nullable=True) 
    id_resm = Column(Integer, ForeignKey('resm.id', ondelete='CASCADE'), nullable=True) 
    id_pos = Column(Integer, ForeignKey('pos.id', ondelete='CASCADE'), nullable=True)     
    
class Education(Base):
    __tablename__='educ'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    id_univ = Column(Integer, ForeignKey('univ.id', ondelete='CASCADE'), nullable=True) 
    id_tedu = Column(Integer, ForeignKey('tedu.id', ondelete='CASCADE'), nullable=True) 
    year_grad = Column(Date, nullable=True)
    specialty = Column(String(255), nullable=True)
    id_resm = Column(Integer, ForeignKey('resm.id', ondelete='CASCADE'), nullable=True)
    id_pos = Column(Integer, ForeignKey('pos.id', ondelete='CASCADE'), nullable=True)    

class Resume(Base):
    __tablename__='resm'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_empl = Column(Integer, nullable=False) 
    e_mail = Column(String, nullable=False)
    id_schd = Column(Integer, ForeignKey('schd.id'), default = 1, nullable=False) 
    id_trip = Column(Integer, ForeignKey('trip.id'), default = 1, nullable=False) 
    post = Column(String(255), nullable=True)
    min_wage = Column(Integer, nullable=True)
    max_wage = Column(Integer, nullable=True)    
    experience = Column(Float, default = 0, nullable=True)
    elan = relationship(EduLang, cascade="all, delete-orphan")
    educ = relationship(Education, cascade="all, delete-orphan")
    rel = relationship(RelationCvPos, cascade="all, delete-orphan")

class Position(Base):
    __tablename__='pos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_pos = Column(Integer, nullable=False) 
    name = Column(String(255), nullable=False)
    info = Column(String(255), nullable=True)    
    e_mail = Column(String, nullable=False)
    id_schd = Column(Integer, ForeignKey('schd.id'), default = 1, nullable=False) 
    id_trip = Column(Integer, ForeignKey('trip.id'), default = 1, nullable=False)     
    min_wage = Column(Integer, nullable=True)
    max_wage = Column(Integer, nullable=True)    
    experience = Column(Float, default = 0, nullable=True)
    elan = relationship(EduLang, cascade="all, delete-orphan")
    educ = relationship(Education, cascade="all, delete-orphan")
    rel = relationship(RelationCvPos, cascade="all, delete-orphan")
   
    
class Schedule(Base):
    __tablename__='schd'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    name = Column(String(255), unique=True, nullable=False)
 
    resm = relationship(Resume)
    pos = relationship(Position)

class IsTrip(Base):
    __tablename__='trip'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  
    name = Column(String(255), unique=True, nullable=False)  
  
    resm = relationship(Resume)
    pos = relationship(Position)

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