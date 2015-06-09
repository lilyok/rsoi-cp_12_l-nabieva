import cherrypy

from database import Empl
import datetime


class UserRequestHandlers(object):

    def __init__(self, database):
        self.__database = database

    @cherrypy.expose
    def register(self, nm, snm, tnm, btd, e_mail, password):
        with self.__database.session() as database_session:
            date = datetime.datetime.strptime(btd, '%d.%m.%Y')
            user = Empl(name=nm, surname=snm, thirdname=tnm, birthday=date, email=e_mail, password=password)
            database_session.add(user)
    
    @cherrypy.expose
    def login(self, e_mail, password):
        with self.__database.session() as database_session:
          user = database_session.query(Empl).filter_by(email=e_mail, password=password).one()
        cherrypy.session['user_id'] = user.id
    
    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()

  
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            user = database_session.query(Empl).get(user_id)

        result  =  {
                    'name': user.name,
                    'surname': user.surname,
                    'thirdname': user.thirdname,
                    }         
        return result #user.surname+' '+user.name+' '+user.thirdname

