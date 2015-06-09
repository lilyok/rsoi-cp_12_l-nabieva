import cherrypy

from database import Universities, Lang, LangLevel, IsTrip, Industry, Schedule
import datetime

class FillingRequestHandlers(object):

    def __init__(self, database):
        self.__database = database

           
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        with self.__database.session() as database_session:
            univ = []
            lang = []
            llev = []
            trip = []
            sphere = []
            schedule = []            
            for instance in database_session.query(Universities).order_by(Universities.id):
                univ.append(instance.name)
            for instance in database_session.query(Lang).order_by(Lang.id):
                lang.append(instance.name)    
            for instance in database_session.query(LangLevel).order_by(LangLevel.id):
                llev.append(instance.name)                  
            for instance in database_session.query(IsTrip).order_by(IsTrip.id):
                trip.append(instance.name)
            for instance in database_session.query(Industry).order_by(Industry.id):
                sphere.append(instance.name)   
            for instance in database_session.query(Schedule).order_by(Schedule.id):
                schedule.append(instance.name)    
                
        result  =  {
                    'trip':trip,
                    'sphere':sphere,
                    'schedule':schedule,
                    'univ':univ,
                    'lang':lang,
                    'llev':llev
                    }         
        return result