import cherrypy

from database import IsTrip, Industry, Schedule
import datetime

class CVRequestHandlers(object):

    def __init__(self, database):
        self.__database = database

           
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        with self.__database.session() as database_session:
            trip = []
            sphere = []
            schedule = []
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
                    }         
        return result