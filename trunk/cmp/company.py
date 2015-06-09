#!/usr/bin/env python

from datetime import datetime
import sys

import cherrypy

from database import Database
from mail_parser import MailParserThread
from filling_request_handlers import FillingRequestHandlers
from position_request_handlers import PositionRequestHandlers

class Company(object):

    def __init__(self):
        self.__database = Database()
        self.fill = FillingRequestHandlers(self.__database)
        self.position = PositionRequestHandlers(self.__database)

        mail_address = cherrypy.config['mail_address']

        self.__mail_thread = MailParserThread(self.__database, mail_address)
        self.__mail_thread.start()

        cherrypy.engine.subscribe(
            'stop', lambda: self.__mail_thread.stop())

    @cherrypy.expose
    def stop_service(self):
        cherrypy.engine.exit()


if __name__ ==  "__main__":

    # if len(sys.argv) < 2:
    #     sys.exit('Usage: ia <config>')

    cherrypy.config.update('company.conf')

    cherrypy.quickstart(Company(), config='company.conf')
