# -*- coding: utf_8 -*-
from datetime import datetime
import email
import json
import cherrypy

from database import Resume, Lang, LangLevel, TypeOfEdu, Universities, IsTrip, Schedule, EduLang, Education, Position , RelationCvPos
from mail_thread import MailThread
from mail_sender import send_as_json
from auto_searcher import AutoSearcher

class MailParserThread(MailThread):

    def __init__(self, database, *args, **kwargs):
        self.__database = database
        MailThread.__init__(self, *args, **kwargs)

    def _process_message(self, message):
        _, sender = email.utils.parseaddr(message['from'])
        content = json.loads(message.get_payload())
        self.__process_parsed_message(sender, content)

    def __process_parsed_message(self, sender, content):
        handlers = { 
            'open_cv': self.open_cv,
            'open_position': self.open_position,
            'denied_pos': self.denied_pos,
            'accept_pos': self.accept_pos,
            'denied_resm': self.denied_resm,
            'accept_resm': self.accept_resm,
            'close': self.close
            }

        action = content.pop('action')
        handlers[action](sender, **content)

    def getIdFromTable(self, tbl, name):
        with self.__database.session() as database_session:
            try:
                cur_id = database_session.query(tbl).filter(tbl.name == name).one().id
            except Exception, e:
                database_session.add(tbl(name = name))
                cur_id = database_session.query(tbl).filter(tbl.name == name).one().id
                database_session.commit() 

        return cur_id

    def add_position(self, sender, pid, pos_name, info, id_schd, id_trip, min_wage, max_wage, experience):
        with self.__database.session() as database_session:        
            try:
                cur_id = database_session.query(Position).filter(Position.id_pos == pid).filter(Position.e_mail == sender).one().id
                print cur_id
                database_session.query(Position).filter(Position.id_pos == pid).filter(Position.e_mail == sender).update({'id_schd': id_schd, 'id_trip':id_trip, 'name':pos_name,
                    'info':info, 'min_wage':min_wage, 'max_wage':max_wage, 'experience':experience})
            except Exception, e:
                database_session.add(Position(id_pos=pid, e_mail=sender, id_schd=id_schd, id_trip=id_trip, 
                name=pos_name, info=info, min_wage=min_wage, max_wage=max_wage, experience=experience))
                cur_id = database_session.query(Position).filter(Position.id_pos == pid).filter(Position.e_mail == sender).one().id
                print cur_id
            return cur_id   

    def add_cv(self, sender, id_empl, id_schd, id_trip, post, min_wage, max_wage, experience):
        with self.__database.session() as database_session:        
            try:
                cur_id = database_session.query(Resume).filter(Resume.id_empl == id_empl).filter(Resume.e_mail == sender).one().id
                print cur_id
                database_session.query(Resume).filter(Resume.id_empl == id_empl).filter(Resume.e_mail == sender).update({'id_schd': id_schd, 'id_trip':id_trip, 'post':post,
                    'min_wage':min_wage, 'max_wage':max_wage, 'experience':experience})
            except Exception, e:
                database_session.add(Resume(id_empl=id_empl, e_mail=sender, id_schd=id_schd, id_trip=id_trip, 
                post=post, min_wage=min_wage, max_wage=max_wage, experience=experience))
                # print id_empl
                # for instance in database_session.query(Resume).filter(Resume.id_empl == id_empl):
                #     print instance.id_empl, instance.experience
                cur_id = database_session.query(Resume).filter(Resume.id_empl == id_empl).filter(Resume.e_mail == sender).one().id

            return cur_id   

    def clear_ei(self, id_resm):
        with self.__database.session() as database_session:
            for instance in database_session.query(Education).filter(Education.id_resm == id_resm):
                database_session.delete(instance)
            for instance in database_session.query(EduLang).filter(EduLang.id_resm == id_resm):
                database_session.delete(instance)
            database_session.commit() 

    def add_edu(self, specialty, id_univ, id_resm = None, id_pos = None, year_grad=None, id_tedu=None):
        if year_grad is not None:
            year_grad = datetime.strptime(year_grad, '%d.%m.%Y').date()
        with self.__database.session() as database_session:        
            try:
                if id_resm is not None:
                    database_session.query(Education).filter(Education.id_resm == id_resm).filter(Education.id_univ==id_univ)\
                    .filter(Education.specialty==specialty).first().id
                if id_pos is not None:    
                    database_session.query(Education).filter(Education.id_pos == id_pos).filter(Education.id_univ==id_univ)\
                    .filter(Education.specialty==specialty).first().id                             
            except Exception, e:
                if id_resm is not None:
                    database_session.add(Education(id_resm=id_resm, specialty=specialty, year_grad=year_grad, 
                    id_tedu=id_tedu, id_univ=id_univ))
                if id_pos is not None:
                    database_session.add(Education(id_pos=id_pos, specialty=specialty, id_univ=id_univ))                    
                database_session.commit() 

    def add_lang(self, id_lang, id_llev, id_resm = None, id_pos = None):
        with self.__database.session() as database_session:        
            try:
                if id_resm is not None:
                    database_session.query(EduLang).filter(EduLang.id_resm == id_resm).filter(EduLang.id_lang==id_lang)\
                    .filter(EduLang.id_llev==id_llev).first().id
                if id_pos is not None:
                    database_session.query(EduLang).filter(EduLang.id_pos == id_pos).filter(EduLang.id_lang==id_lang)\
                    .filter(EduLang.id_llev==id_llev).first().id                    
            except Exception, e:
                if id_resm is not None:
                    database_session.add(EduLang(id_resm=id_resm, id_lang=id_lang, id_llev=id_llev))
                if id_pos is not None:
                    database_session.add(EduLang(id_pos=id_pos, id_lang=id_lang, id_llev=id_llev))                    
                database_session.commit() 


    def open_cv(self, sender, eid, post, min_wage, max_wage, exp, sch, trp, univ, tedu, year_grad, specialty, lang, llev):#, schedule=None, trip=None, post=None, min_wage=None, max_wage=None, skills='', exp=None):
        try:
            print "open_cv"
            print eid, post, min_wage, max_wage, exp, sch, trp
            print "start open_cv"
            id_schd = self.getIdFromTable(Schedule, sch)
            id_trip = self.getIdFromTable(IsTrip, trp)
            id_resm = self.add_cv(sender, eid, id_schd, id_trip, post, min_wage, max_wage, exp)
            if univ is not None:
                for i in range(len(univ)):
                    id_univ = self.getIdFromTable(Universities, univ[i])
                    id_tedu = self.getIdFromTable(TypeOfEdu, tedu[i])
                    self.add_edu(id_resm=id_resm, specialty=specialty[i], year_grad=year_grad[i], id_tedu=id_tedu, id_univ=id_univ)
            if lang is not None:
                for i in range(len(lang)):
                    id_lang = self.getIdFromTable(Lang, lang[i])
                    id_llev = self.getIdFromTable(LangLevel, llev[i])
                    self.add_lang(id_resm=id_resm, id_lang=id_lang, id_llev=id_llev)
           
            asch = AutoSearcher(self.__database)  
            print "SEARCH!!!!!!!!!" 
            asch.__SearchPos__(sender, id_resm, eid, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev)         
       
        except Exception, e:
            print e

    def open_position(self, sender, pid, pos_name, info, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev):#, schedule=None, trip=None, post=None, min_wage=None, max_wage=None, skills='', exp=None):
        try:
            print pid, pos_name, min_wage, max_wage, exp, sch, trp
            print univ[0], specialty[0]
            # with self.__database.session() as database_session:
            id_schd = self.getIdFromTable(Schedule, sch)
            id_trip = self.getIdFromTable(IsTrip, trp)
            id_pos = self.add_position(sender, pid, pos_name, info, id_schd, id_trip, min_wage, max_wage, exp)

            if univ is not None:
                for i in range(len(univ)):
                    id_univ = self.getIdFromTable(Universities, univ[i])
                    print specialty
                    print specialty[i]
                    self.add_edu(id_pos=id_pos, specialty=specialty[i], id_univ=id_univ)
            if lang is not None:
                for i in range(len(lang)):
                    id_lang = self.getIdFromTable(Lang, lang[i])
                    id_llev = self.getIdFromTable(LangLevel, llev[i])
                    self.add_lang(id_pos=id_pos, id_lang=id_lang, id_llev=id_llev)
            asch = AutoSearcher(self.__database)  
            print "SEARCH for pos!!!!!!!!!" 
            asch.__SearchResm__(id_pos)                    
        except Exception, e:
            print e

    def denied_pos(self, sender, id_pos, id_empl):
        try:        
            with self.__database.session() as database_session:  
                resm_id = database_session.query(Resume).filter(Resume.id_empl == id_empl).filter(Resume.e_mail == sender).one().id
                print resm_id

                print id_pos
                # pos_id = database_session.query(Position).filter(Position.id_pos == id_pos).filter(Position.e_mail == e_mail_pos).one().id
                # print pos_id
                rel = database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == resm_id).filter(RelationCvPos.id_pos == id_pos).one()
                print rel
                old_status =  rel.status
                rel.status = 0
                database_session.commit() 
                print rel.status

                if(old_status < 0):
                    pos = database_session.query(Position).get(id_pos)
                    recipient_address = pos.e_mail
      
                    
                    content={
                        'id':resm_id,
                        'id_pos': pos.id_pos,
                        'status': 0
                    }
                    sender_address = cherrypy.config['mail_address']                
                    send_as_json(sender_address, recipient_address, content)      

        except Exception, e:
            print e

    @cherrypy.expose
    def accept_pos(self, sender, id_pos, id_empl, name, skills, email = None):
        print "____accept_pos_____"
        try:        
            with self.__database.session() as database_session:  
                resm_id = database_session.query(Resume).filter(Resume.id_empl == id_empl).filter(Resume.e_mail == sender).one().id
                rel = database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == resm_id).filter(RelationCvPos.id_pos == id_pos).one()

                print "old status", rel.status
                if rel.status > 0:
                    rel.status = -1
                elif rel.status != 0 and abs(rel.status) % 2 == 0:
                    rel.status -= 1
                database_session.commit(); 
                print "new status", rel.status
                resm = database_session.query(Resume).get(resm_id)

                lan = []
                for elan in database_session.query(EduLang).filter(EduLang.id_resm == resm_id):
                    lan.append(database_session.query(Lang).filter(Lang.id == elan.id_lang).one().name +" - "+ database_session.query(LangLevel).filter(LangLevel.id == elan.id_llev).one().name)
                educ=[]
                for eeduc in database_session.query(Education).filter(Education.id_resm == resm_id):
                    educ.append(database_session.query(Universities).filter(Universities.id == eeduc.id_univ).one().name +": "+ eeduc.specialty)
                print "start content"
                content = {
                    'id': resm_id,
                    'name': name,
                    'e_mail': sender,
                    'post': resm.post,
                    'skills': skills,
                    'exp':resm.experience,
                    'wage': str(resm.min_wage)+"-"+str(resm.max_wage),
                    'schd': database_session.query(Schedule).get(resm.id_schd).name,
                    'trip': database_session.query(IsTrip).get(resm.id_trip).name,
                    'lan':lan, 
                    'educ': educ,
                    'id_pos': database_session.query(Position).get(id_pos).id_pos,
                    'status': rel.status 
                }  
                print email 
                if email:
                    content['email'] = email
                else:
                    content['email'] = 'будет предоставлен после согласия пройти собеседование'
                print "stop content"
                recipient_address = database_session.query(Position).get(id_pos).e_mail
                sender_address = cherrypy.config['mail_address']
                print recipient_address, sender_address
                send_as_json(sender_address, recipient_address, content) 
        except Exception, e:
            print e

    def denied_resm(self, sender, id_pos, id_resm):
        try:        
            with self.__database.session() as database_session:  
                print id_pos
                print id_resm
                eid = database_session.query(Resume).get(id_resm).id_empl
                pos_id = database_session.query(Position).filter(Position.id_pos == id_pos).filter(Position.e_mail == sender).one().id
                recipient_address = database_session.query(Resume).get(id_resm).e_mail
                rel = database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == id_resm).filter(RelationCvPos.id_pos == pos_id).one()
                print rel
                print rel.status
                rel.status = 0
                database_session.commit() 
                print rel.status
                
                content = []
                content.append({
                    'id':id_pos,
                    'eid': eid,
                    'status': 0
                })
                sender_address = cherrypy.config['mail_address']                
                send_as_json(sender_address, recipient_address, content)
        except Exception, e:
            print e

    def accept_resm(self, sender, id_pos, id_resm, status):
        try:
            with self.__database.session() as database_session:  
                print id_pos
                print id_resm
                eid = database_session.query(Resume).get(id_resm).id_empl      
                pos_id = database_session.query(Position).filter(Position.id_pos == id_pos).filter(Position.e_mail == sender).one().id
                recipient_address = database_session.query(Resume).get(id_resm).e_mail
                rel = database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == id_resm).filter(RelationCvPos.id_pos == pos_id).one()
                print rel
                print rel.status
                rel.status = status
                database_session.commit() 
                print rel.status
                
                content = []
                content.append({
                    'id':id_pos,
                    'eid': eid,
                    'status': status
                })
                sender_address = cherrypy.config['mail_address']                
                send_as_json(sender_address, recipient_address, content)
        except Exception, e:
            print e


    def close(self, sender, id):
        print "close"
        try:        
            with self.__database.session() as database_session:  
                print id
                sender_address = cherrypy.config['mail_address']
                pos_id = database_session.query(Position).filter(Position.id_pos == id).filter(Position.e_mail == sender).one().id
                print pos_id
                for rel in database_session.query(RelationCvPos).filter(RelationCvPos.id_pos == pos_id):
                    recipient_address = database_session.query(Resume).get(rel.id_resm).e_mail
                    content = []
                    content.append({
                        'id':pos_id,
                        'eid': database_session.query(Resume).get(rel.id_resm).id_empl,
                        'status': -6
                    })
                    send_as_json(sender_address, recipient_address, content)
                    database_session.delete(rel)
        except Exception, e:
            print e