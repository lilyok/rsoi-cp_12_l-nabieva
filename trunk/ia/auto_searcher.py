# -*- coding: utf_8 -*-
import re
import cherrypy
from database import Resume, Lang, LangLevel, Universities, IsTrip, Schedule, EduLang, Education, Position, RelationCvPos
from sqlalchemy import desc
from mail_sender import send_as_json

class AutoSearcher():

    def __init__(self, database, *args, **kwargs):
        self.__database = database

    def __getId__(self, tbl, name):
        with self.__database.session() as database_session:
            return database_session.query(tbl).filter(tbl.name == name).one().id

    def __getLang__(self, pos_id):
        lang = []
        llev = []
        with self.__database.session() as database_session:
            for instance in database_session.query(EduLang).filter(EduLang.id_pos == pos_id):
                lang.append(instance.id_lang)
                llev.append(instance.id_llev)
        return [lang, llev]

    def __getUniv__(self, pos_id):
        univ = []
        spec = []
        with self.__database.session() as database_session:
            for instance in database_session.query(Education).filter(Education.id_pos == pos_id):
                univ.append(instance.id_univ)
                spec.append(instance.specialty)
        return [univ, spec]

    def __getResultSatisfaction__(self, query, result):
        # the result have to cover query
        rx = re.compile("[^\W\d]+", re.UNICODE)
        qArr = rx.findall(query.lower())
        rArr = rx.findall(result.lower())

        n = 0.0
        for a in qArr:
            if a in rArr:
                n += 1
        if n/len(qArr) > 0.4:
            return True
        else:
            return False

    def __CreateCriterion__(self, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev):
        print "Really SEARCH START" 
        coefTbl = {}
        max_coef = 11.0
        print post
        with self.__database.session() as database_session:
            for instance in database_session.query(Position):
                coef = 0.0
                if (instance.experience <= float(exp)):
                    coef += 1

                if (instance.max_wage >= int(min_wage)):
                    coef += 1

                if ((trp == u'готов') or (self.__getId__(IsTrip, trp) == instance.id_trip)) :
                    coef += 1
                if ((sch == u'полный день') or (self.__getId__(Schedule, sch) == instance.id_schd)):
                    coef += 1
                if self.__getResultSatisfaction__(post, instance.name): coef += 1

                [lng, llv] = self.__getLang__(instance.id)
                lng_coef = len(lng)
                if lang is not None:
                    for i in range(len(lang)):
                        id_lang = self.__getId__(Lang, lang[i])
                        if (id_lang in lng):
                            lng_coef -= 1

                if (lng_coef < len(lng)): coef += 1;
                if (lng_coef <= 0): coef += 1;

                [unv, spc] = self.__getUniv__(instance.id)
                univ_coef = len(unv)
                spec_coef = univ_coef
                if univ is not None:
                    for i in range(len(univ)):
                        id_univ = self.__getId__(Universities, univ[i])
                        if (id_univ in unv):
                            univ_coef -= 1

                        if self.__getResultSatisfaction__(spc[i], specialty[i]): spec_coef -= 1;

                if (univ_coef < len(unv)): coef += 1;
                if (univ_coef <= 0): coef += 1;
                if (spec_coef < len(spc)): coef += 1;
                if (spec_coef <= 0): coef += 1;
  
                coefTbl[instance.id] = coef / max_coef


        return coefTbl;
    
    @cherrypy.expose
    def __NotifyUser__(self, id_resm, eid, sender):
        print "__NotifyUser__"

        positionsNotify = []
        with self.__database.session() as database_session:
            # e_mail = database_session.query(Resume).filter(Resume.id == id_resm).one().e_mail
            # print "e_mail=",e_mail
            for instance in database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == id_resm).order_by(desc(RelationCvPos.status)):
                # print instance.id, instance.id_resm, instance.id_pos, instance.status
                if instance.status != 0.0:
                    position = database_session.query(Position).filter(Position.id == instance.id_pos).one()
                    lan = []
                    for elan in database_session.query(EduLang).filter(EduLang.id_pos == position.id):
                       lan.append(database_session.query(Lang).filter(Lang.id == elan.id_lang).one().name +" - "+ database_session.query(LangLevel).filter(LangLevel.id == elan.id_llev).one().name)
                    # print lan  
                    educ =[]
                    for eeduc in database_session.query(Education).filter(Education.id_pos == position.id):
                        educ.append(database_session.query(Universities).filter(Universities.id == eeduc.id_univ).one().name +": "+ eeduc.specialty)
                    # print educ

                    positionsNotify.append({'id':position.id,'name': position.name, 'info':position.info, 
                        'schd':database_session.query(Schedule).filter(Schedule.id == position.id_schd).one().name, 
                        'trip':database_session.query(IsTrip).filter(IsTrip.id == position.id_trip).one().name, 
                        'min_wage':position.min_wage, 'max_wage':position.max_wage, 'experience':position.experience, 
                        'lan':lan, 'educ': educ, 'eid':eid, 'status':instance.status})

        print "positionsNotify"
        # print positionsNotify

        sender_address = cherrypy.config['mail_address']
        print sender_address, sender
        send_as_json(sender_address, sender, positionsNotify)   
        # вот тут будет отсылка сендеру positionsNotify и еид 


    def __AddRelationCvPos__(self, id_resm, pid, coef):
        print "__addRelationCvPos__"
        with self.__database.session() as database_session:
            try:
                r = database_session.query(RelationCvPos).filter(RelationCvPos.id_pos == pid).filter(RelationCvPos.id_resm == id_resm).one()
                # print r.id
                # print "!!!!!!!!!!!!!!!!"
                print r.status, coef
                if (r.status is None) or (r.status != float(coef))and(r.status >= 0.0):
                    # print "!!!!!!!!!!!!!!!!"
                    r.status = coef
                    print r.status, coef
                    database_session.add(r)
            except Exception, e:
                database_session.add(RelationCvPos(id_pos=pid, id_resm=id_resm, status = coef)) 



    def __SearchPos__(self, sender, id_resm, eid, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev):
        print "SEARCH START" 
        coefTbl = self.__CreateCriterion__(post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev)
        for id_pos, coef in coefTbl.items():
            if coef >= 0.4 :
                print id_pos, coef
                self.__AddRelationCvPos__(id_resm, id_pos, coef)

        self.__NotifyUser__(id_resm, eid, sender)
        # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        # print coefTbl

 # написать запрос, берущий позиции из position, если удовл всем критериям 

if __name__ == '__main__':
    aus = AutoSearcher(None)
    aus.__getResultSatisfaction__(u'привет, мир! "мама": мыла раму',u'Привет, мама =); панараму мыла ламу?')