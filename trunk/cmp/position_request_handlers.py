# -*- coding: utf_8 -*-

import cherrypy

from mail_sender import send_as_json
import datetime
from database import IsTrip, Schedule, Education, Universities, Position, Lang, LangLevel, EduLang

class PositionRequestHandlers(object):

    def __init__(self, database):
        self.__database = database

        # handlers = {  сделать тут распределение портов IA от названий
        # 'open_cv': self.open_cv#,
        # # 'resond_position': pass, 
        # # 'reject_position': pass, 
        # # 'reject_offer': pass,
        # # 'accept_offer': pass,
        # # 'open_position': pass,
        # # 'update_position': pass,
        # # 'close_position': pass,
        # # 'reject': pass,
        # # 'offer': pass
        # }

           
    @cherrypy.expose
    def clear(self, pos_id):
        print pos_id
        with self.__database.session() as database_session:
            for instance in database_session.query(Position).filter(Position.id == pos_id):
                print instance.name
                database_session.delete(instance)
            database_session.commit()               

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAbout(self):    
        company = {}
        with open("info.txt") as rows:
            isFirst = True
            about = ''
            for line in rows:
                if isFirst:
                    company['data'] = str(line.strip())
                    isFirst = False 
                else:
                    about += line;
            company['about'] = about   
        return company

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getExists(self):
        positions = []
        with self.__database.session() as database_session:
            for instance in database_session.query(Position):
                pos = {}
                pos['name'] = instance.name
                pos['info'] = instance.info                
                pos['min_wage'] = instance.min_wage
                pos['max_wage'] = instance.max_wage
                pos['experience'] = instance.experience
                pos['id_inds'] = instance.id_inds                                               
                pos['id_schd'] = instance.id_schd                
                pos['id_trip'] = instance.id_trip
                pos['educ'] = []                

                pos['educ'] = []
                for ed in database_session.query(Education).filter(Education.id_pos == instance.id):
                    pos['educ'].append({'id_univ':ed.id_univ, 'specialty': ed.specialty})

                pos['lang'] = []
                for lng in database_session.query(EduLang).filter(EduLang.id_pos == instance.id):
                    pos['lang'].append({'id_lang':lng.id_lang, 'id_llev': lng.id_llev})

                positions.append(pos)   
        return positions

    @cherrypy.expose  
    def save_about(self, date, about='', ):
        f = open( 'info.txt', 'w' )
        f.write(date+'\n')
        f.write(about.encode('utf8').strip())                    
        f.close()       

    @cherrypy.expose
    def save(self, pos_id, num_edu, num_lang, id_sphere=None, id_schedule=None, info ='', id_trip=None, min_wage=0, max_wage=0,pos_name ='', pos_info='', exp=0.0,lang_ids=None, llev_ids=None, univ_ids=None, specialities=None): #save education info
        self.clear(pos_id)
        with self.__database.session() as database_session:
            if((id_schedule is not None) and (id_sphere is not None) and (id_trip is not None)):

                database_session.add(Position(id=pos_id, name=pos_name, id_inds=id_sphere, info= info, id_schd=id_schedule, id_trip=id_trip, 
                        min_wage=min_wage, max_wage=max_wage, experience=exp))
                database_session.commit()

                if(univ_ids is not None):
                    i = 0
                    while i < int(num_edu):
                        if int(num_edu) == 1:
                            spec = specialities
                            idUniv = univ_ids
                        else:
                            spec = specialities[i]
                            idUniv = univ_ids[i]
                        database_session.add(Education(id_univ = idUniv, specialty = spec, id_pos = pos_id))
                        i+=1
                    database_session.commit()    
                if(llev_ids is not None):
                    i = 0          
                    while i < int(num_lang):
                        if int(num_lang) == 1:
                            langId = lang_ids
                            llevId = llev_ids
                        else:
                            langId = lang_ids[i]
                            llevId = llev_ids[i]            
                        database_session.add(EduLang(id_lang = langId, id_llev = llevId, id_pos = pos_id))
                        i+=1           
                    database_session.commit()

                self.open_position( num_edu, num_lang, pos_id, id_sphere, id_schedule, id_trip, pos_name, info, min_wage, max_wage, exp, lang_ids, llev_ids, univ_ids, specialities)

    @cherrypy.expose
    def open_position(self, num_edu, num_lang, pid=None, id_sphere=None, id_schedule=None, id_trip=None, pos_name='', info = '', min_wage=None, max_wage=None, exp=None,lang_ids=None, llev_ids=None, univ_ids=None, specialities=None):
        sender_address = cherrypy.config['mail_address']
        mail_address = 'mbox1274-11@dev.iu7.bmstu.ru'
        print "open_position"
        with self.__database.session() as database_session:
            sch = database_session.query(Schedule).filter_by(id=id_schedule).one().name
            trp = database_session.query(IsTrip).filter_by(id=id_trip).one().name
            univ = []
            specialty = []
            lang = []
            llev = []

            if lang_ids is not None:
                for i in range(int(num_lang)):
                    lang.append(database_session.query(Lang).filter(Lang.id == lang_ids[i]).one().name)
                    llev.append(database_session.query(LangLevel).filter(LangLevel.id == llev_ids[i]).one().name)
            if univ_ids is not None:
                for i in range(int(num_edu)):
                    print i
                    univ.append(database_session.query(Universities).filter(Universities.id == univ_ids[i]).one().name)   
                    print specialities
                    print univ_ids
                    if int(num_lang) > 1:
                        specialty.append(specialities[i])
                    else:
                        specialty.append(specialities)                        
            print specialty

            content = {
                'action': 'open_position',
                'pid': pid,
                'pos_name': pos_name,
                'info': info,                
                'min_wage':min_wage,
                'max_wage':max_wage, 
                'exp':exp, 
                'sch':sch,
                'trp':trp,
                'univ':univ,
                'specialty':specialty,
                'lang':lang,
                'llev':llev
                }
            send_as_json(sender_address, mail_address, content)    