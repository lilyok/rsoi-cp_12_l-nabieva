#!/usr/bin/env python

from datetime import datetime
import sys

import cherrypy

from database import Database
from mail_parser import MailParserThread


class IndustryAssociation(object):

    def __init__(self):
        self.__database = Database()

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

    cherrypy.config.update('ia.conf')

    cherrypy.quickstart(IndustryAssociation())
