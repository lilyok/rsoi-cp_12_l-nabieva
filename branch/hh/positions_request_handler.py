import cherrypy
from sqlalchemy import desc

from database import Positions, Empl, Resume
from mail_sender import send_as_json

import datetime

class PositionsRequestHandlers(object):

    def __init__(self, database):
        self.__database = database
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def accept(self, id):
        print "___accept___"
        sender_address = cherrypy.config['mail_address']  
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            pos = database_session.query(Positions).get(id)
            print "status: ", pos.status
            if pos.status > 0:
                pos.status = -1
            elif pos.status != 0 and abs(pos.status) % 2 == 0:
                pos.status -= 1
            name = database_session.query(Empl).get(user_id)

            skills = ''
            for resm in database_session.query(Resume).filter(Resume.id_empl == user_id):
                skills += resm.skills + "; "
            content = {
                'action': 'accept_pos',
                'id_pos': pos.id_pos,
                'id_empl': user_id,
                'name': name.surname + " " + name.name +" "+ name.thirdname,
                'skills': skills  
            }         
            print pos.status, name.email
            if (pos.status == -3):
                content['email'] = name.email

            send_as_json(sender_address, pos.e_mail, content)    
            database_session.commit()
            print pos.status
            return pos.status        
 
    @cherrypy.expose
    def deleted(self, id):
        with self.__database.session() as database_session:
            pos = database_session.query(Positions).get(id)
            database_session.delete(pos)               

    @cherrypy.expose
    def denied(self, id):
        sender_address = cherrypy.config['mail_address']
        user_id = cherrypy.session.get('user_id')

        with self.__database.session() as database_session:
            pos = database_session.query(Positions).get(id)
            content = {
                'action': 'denied_pos',
                'id_pos': pos.id_pos,
                'id_empl': user_id                
            }
            send_as_json(sender_address, pos.e_mail, content)
            database_session.delete(pos)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        user_id = cherrypy.session.get('user_id')
        result = []
        with self.__database.session() as database_session:
            for instance in database_session.query(Positions).filter(Positions.id_empl == user_id).order_by(desc(Positions.status)):
                result.append({'id': instance.id,'name': instance.name, 'info': instance.info, 'schd': instance.schd, 
                    'trip': instance.trip, 'min_wage': instance.min_wage, 'max_wage': instance.max_wage, 
                    'experience': instance.experience, 'lan': instance.lan, 'educ': instance.educ, 'status': instance.status})
      
        return result