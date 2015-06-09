# -*- coding: utf_8 -*-

import cherrypy

from database import Resume
from mail_sender import send_as_json
import datetime
from database import IsTrip, Schedule, Education, Universities, TypeOfEdu, Lang, LangLevel, EduLang

class UserCVRequestHandlers(object):

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
    def clear_cv(self):
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            for instance in database_session.query(Resume).filter(Resume.id_empl == user_id):
                database_session.delete(instance)
            database_session.commit()               


    @cherrypy.expose
    def save_cv(self, num_resume, id_sphere=None, id_schedule=None, id_trip=None, post=None, min_wage=None, max_wage=None, skills='', exp=None): #save education info
        self.clear_cv()
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            if((id_schedule is not None) and (id_sphere is not None) and (id_trip is not None) and (exp is not None)):
                i = 0
                while i < int(num_resume):
                    if int(num_resume) == 1:
                        id_sph = id_sphere
                        id_sch = id_schedule
                        id_trp = id_trip
                        pst = post
                        min_w = min_wage
                        max_w = max_wage
                        sklls = skills
                        experience = exp                   
                    else:
                        id_sph = id_sphere[i]
                        id_sch = id_schedule[i]
                        id_trp = id_trip[i]
                        pst = post[i]
                        min_w = min_wage[i]
                        max_w = max_wage[i]
                        sklls = skills[i]
                        experience = exp[i] 

                    database_session.add(Resume(id_inds=id_sph, id_schd=id_sch, id_trip=id_trp, post=pst, 
                        min_wage=min_w, max_wage=max_w, skills=sklls, experience=experience, id_empl=user_id))
                    i+=1
                    database_session.commit()
                    self.open_cv(user_id, id_sph, id_sch, id_trp, pst, min_w, max_w, experience)

                # database_session.commit()
                # self.open_cv(user_id, id_schedule, id_trip, post, min_wage, max_wage, exp)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        user_id = cherrypy.session.get('user_id')
        num_resume = 0
        with self.__database.session() as database_session:
            result = {'id_trip':[], 'id_sphere':[], 'id_schedule':[], 'post':[], 'min_wage':[], 'max_wage':[], 'skills':[], 'exp':[]}
            
            for instance in database_session.query(Resume).filter(Resume.id_empl == user_id):
                result['id_sphere'].append(instance.id_inds-1)
                result['id_schedule'].append(instance.id_schd-1)
                result['id_trip'].append(instance.id_trip-1)     
                result['post'].append(instance.post)           
                result['min_wage'].append(instance.min_wage)   
                result['max_wage'].append(instance.max_wage)        
                result['skills'].append(instance.skills) 
                result['exp'].append(instance.experience)    
                num_resume+=1;  
        result['num_resume'] = num_resume
                
        return result

    @cherrypy.expose
    def open_cv(self, eid=None, id_sphere=None, id_schedule=None, id_trip=None, post=None, min_wage=None, max_wage=None, exp=None):
        sender_address = cherrypy.config['mail_address']
        mail_address = 'mbox1274-11@dev.iu7.bmstu.ru'

        with self.__database.session() as database_session:
            sch = database_session.query(Schedule).filter_by(id=id_schedule).one().name
            trp = database_session.query(IsTrip).filter_by(id=id_trip).one().name
            univ = []
            tedu = []
            year_grad = []
            specialty = []
            lang = []
            llev = []
            # userfk =  {'univ':[], 'tedu':[], 'year_grad':[], 'specialty':[], 'lang':[], 'llev':[]}

            for instance in database_session.query(Education).filter(Education.id_empl == eid):
                univ.append(database_session.query(Universities).filter(Universities.id == instance.id_univ).one().name)
                tedu.append(database_session.query(TypeOfEdu).filter(TypeOfEdu.id == instance.id_tedu).one().name)
                year_grad.append(str(instance.year_grad.strftime("%d.%m.%Y")))
                specialty.append(instance.specialty)  
            for instance in database_session.query(EduLang).filter(EduLang.id_empl == eid):
                lang.append(database_session.query(Lang).filter(Lang.id == instance.id_lang).one().name)
                llev.append(database_session.query(LangLevel).filter(LangLevel.id == instance.id_llev).one().name)
              


            content = {
                'action': 'open_cv',
                'eid': eid,
                'post': post,
                'min_wage':min_wage,
                'max_wage':max_wage, 
                'exp':exp, 
                'sch':sch,
                'trp':trp,
                'univ':univ,
                'tedu':tedu,
                'year_grad':year_grad,
                'specialty':specialty,
                'lang':lang,
                'llev':llev
                }
            send_as_json(sender_address, mail_address, content)        