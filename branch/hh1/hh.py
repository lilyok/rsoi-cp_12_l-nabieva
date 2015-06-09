#!/usr/bin/env python

import cherrypy
import sys

from database import Database, Empl
from education_request_handlers import EducationRequestHandlers
from user_request_handlers import UserRequestHandlers
from usereduc_request_handlers import UserEducHandlers
from cv_request_handlers import CVRequestHandlers
from usercv_request_handlers import UserCVRequestHandlers
from mail_parser import MailParserThread
from positions_request_handler import PositionsRequestHandlers

class CreateResume(object):
    def show_database(self):
        with self.__database.session() as database_session:
        # посмотрим что уже есть в базе данных
            for instance in database_session.query(Empl).order_by(Empl.id):
                print instance
                
    def __init__(self):
        self.__database = Database()
        self.__database.create_tables()
        self.show_database()
        self.user = UserRequestHandlers(self.__database)
        self.education = EducationRequestHandlers(self.__database)
        self.usereduc = UserEducHandlers(self.__database)
        self.usercv = UserCVRequestHandlers(self.__database)
        self.cv = CVRequestHandlers(self.__database)
        self.positions = PositionsRequestHandlers(self.__database)
        mail_address = cherrypy.config['mail_address']

        self.__mail_thread = MailParserThread(self.__database, mail_address)
        self.__mail_thread.start()

        cherrypy.engine.subscribe(
            'stop', lambda: self.__mail_thread.stop())
  
    @cherrypy.expose
    def stop_service(self):
        cherrypy.engine.exit()

if __name__ ==  "__main__":
    cherrypy.config.update('hh.conf')
    
    cherrypy.quickstart(
        CreateResume(), config='hh.conf')
