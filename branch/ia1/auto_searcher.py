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
        print "__getId__"
        print  tbl, name
        with self.__database.session() as database_session:
            return database_session.query(tbl).filter(tbl.name == name).one().id
        return -1    

    def __getLang__(self, pos_id):
        print "__getLang__"
        lang = []
        llev = []
        with self.__database.session() as database_session:
            for instance in database_session.query(EduLang).filter(EduLang.id_pos == pos_id):
                lang.append(instance.id_lang)
                llev.append(instance.id_llev)
        return [lang, llev]

    def __getUniv__(self, pos_id):
        print "__getUniv__"
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

    def __CreateCriterionForCurPos(self, instance, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev):
        print "__CreateCriterionForCurPos"
        max_coef = 11.0
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

        print instance.id
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

        # coefTbl[instance.id] = coef / max_coef
        return coef / max_coef

    def __CreateCriterion__(self, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev):
        print "Really SEARCH START" 
        coefTbl = {}
        print post
        with self.__database.session() as database_session:
            for instance in database_session.query(Position):
                coefTbl[instance.id] = self.__CreateCriterionForCurPos(instance, post, min_wage, max_wage, exp, sch, trp, univ, specialty, lang, llev)#coef / max_coef

        return coefTbl;
    
    def __getPositionInfo(self, id_pos, database_session):
        position = database_session.query(Position).get(id_pos)
        lan = []
        for elan in database_session.query(EduLang).filter(EduLang.id_pos == position.id):
           lan.append(database_session.query(Lang).filter(Lang.id == elan.id_lang).one().name +" - "+ database_session.query(LangLevel).filter(LangLevel.id == elan.id_llev).one().name)
        educ =[]
        for eeduc in database_session.query(Education).filter(Education.id_pos == position.id):
            educ.append(database_session.query(Universities).filter(Universities.id == eeduc.id_univ).one().name +": "+ eeduc.specialty)
        return [position, lan, educ]


    @cherrypy.expose
    def __NotifyUser__(self, id_resm, eid, sender):
        print "__NotifyUser__"

        positionsNotify = []
        with self.__database.session() as database_session:
            for instance in database_session.query(RelationCvPos).filter(RelationCvPos.id_resm == id_resm).order_by(desc(RelationCvPos.status)):
                if instance.status != 0.0:
                    [position, lan, educ] = self.__getPositionInfo(instance.id_pos, database_session)#database_session.query(Position).filter(Position.id == instance.id_pos).one()

                    positionsNotify.append({'id':position.id,'name': position.name, 'info':position.info, 
                        'schd':database_session.query(Schedule).filter(Schedule.id == position.id_schd).one().name, 
                        'trip':database_session.query(IsTrip).filter(IsTrip.id == position.id_trip).one().name, 
                        'min_wage':position.min_wage, 'max_wage':position.max_wage, 'experience':position.experience, 
                        'lan':lan, 'educ': educ, 'eid':eid, 'status':instance.status})

        print "positionsNotify"
        print positionsNotify

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
            print id_pos, coef 
            if coef >= 0.4 :
                print id_pos, coef
                self.__AddRelationCvPos__(id_resm, id_pos, coef)

        self.__NotifyUser__(id_resm, eid, sender)

    def __getULang__(self, id_resm):
        print "__getULang__"
        lang = []
        llev = []
        with self.__database.session() as database_session:
            for instance in database_session.query(EduLang).filter(EduLang.id_resm == id_resm):
                lang.append(database_session.query(Lang).get(instance.id_lang).name)
                llev.append(database_session.query(LangLevel).get(instance.id_llev).name)
        return [lang, llev]

    def __getUUniv__(self, id_resm):
        print "__getUUniv__"
        univ = []
        spec = []
        with self.__database.session() as database_session:
            for instance in database_session.query(Education).filter(Education.id_resm == id_resm):
                univ.append(database_session.query(Universities).get(instance.id_univ).name)
                spec.append(instance.specialty)
        return [univ, spec]

    def __CreateCriterionForPos__(self, id_pos):
        print "Really SEARCH START" 
        coefTbl = {}

        with self.__database.session() as database_session:
            pos = database_session.query(Position).get(id_pos)
            for r in database_session.query(Resume):
                [lng, llv] = self.__getULang__(r.id)
                [unv, spc] = self.__getUUniv__(r.id)
                sch = database_session.query(Schedule).get(r.id_schd).name
                trp = database_session.query(IsTrip).get(r.id_trip).name
                print "lng", lng
                coefTbl[r.id] = self.__CreateCriterionForCurPos(pos, r.post, r.min_wage, r.max_wage, r.experience, sch, trp, unv, spc, lng, llv)
        return coefTbl;

    def __Notify_Users__(self, sender_address, id_res, id_pos, status):
        positionsNotify = []
        with self.__database.session() as database_session:
            eid = database_session.query(Resume).get(id_res).id_empl
            sender = database_session.query(Resume).get(id_res).e_mail
            [position, lan, educ] = self.__getPositionInfo(id_pos, database_session)
            positionsNotify.append({'id':position.id,'name': position.name, 'info':position.info, 
                'schd':database_session.query(Schedule).filter(Schedule.id == position.id_schd).one().name, 
                'trip':database_session.query(IsTrip).filter(IsTrip.id == position.id_trip).one().name, 
                'min_wage':position.min_wage, 'max_wage':position.max_wage, 'experience':position.experience, 
                'lan':lan, 'educ': educ, 'eid':eid, 'status':status})

            print "positionsNotify"
            print positionsNotify

            # sender_address = cherrypy.config['mail_address']
            print sender_address, sender
            send_as_json(sender_address, sender, positionsNotify)          

    def __SearchResm__(self, id_pos):
        print "SEARCH RESUME START"
        coefTbl =  self.__CreateCriterionForPos__(id_pos)
        sender_address = cherrypy.config['mail_address']
        for id_res, coef in coefTbl.items():
            print id_res, coef 
            if coef >= 0.4 :
                print id_res, coef
                self.__AddRelationCvPos__(id_res, id_pos, coef)
                self.__Notify_Users__(sender_address, id_res, id_pos, coef)
 


if __name__ == '__main__':
    aus = AutoSearcher(None)
    aus.__getResultSatisfaction__(u'привет, мир! "мама": мыла раму',u'Привет, мама =); панараму мыла ламу?')