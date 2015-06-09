import cherrypy

from database import Universities, TypeOfEdu, Lang, LangLevel
import datetime

class EducationRequestHandlers(object):

    def __init__(self, database):
        self.__database = database

           
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        with self.__database.session() as database_session:
            univ = []
            tedu = []
            lang = []
            llev = []
            for instance in database_session.query(Universities).order_by(Universities.id):
                univ.append(instance.name)
            for instance in database_session.query(TypeOfEdu).order_by(TypeOfEdu.id):
                tedu.append(instance.name)   
            for instance in database_session.query(Lang).order_by(Lang.id):
                lang.append(instance.name)    
            for instance in database_session.query(LangLevel).order_by(LangLevel.id):
                llev.append(instance.name)                  
                
        result  =  {
                    'univ':univ,
                    'tedu':tedu,
                    'lang':lang,
                    'llev':llev,
                    }         
        return result