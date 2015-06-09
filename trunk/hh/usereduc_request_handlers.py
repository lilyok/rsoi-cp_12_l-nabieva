import cherrypy

from database import Education, EduLang
import datetime


class UserEducHandlers(object):

    def __init__(self, database):
        self.__database = database

    @cherrypy.expose
    def clear_ei(self):
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            for instance in database_session.query(Education).filter(Education.id_empl == user_id):
                database_session.delete(instance)
            for instance in database_session.query(EduLang).filter(EduLang.id_empl == user_id):
                database_session.delete(instance)
            database_session.commit()               



    @cherrypy.expose
    def save_ei(self, num_edu, num_lang, lang_ids=None, llev_ids=None, univ_ids=None, specialities=None, year_grads=None, tedu_ids=None): #save education info
        self.clear_ei()
        user_id = cherrypy.session.get('user_id')
        with self.__database.session() as database_session:
            if(univ_ids is not None):
                i = 0
                while i < int(num_edu):
                    if int(num_edu) == 1:
                        idTedu = tedu_ids
                        idUniv = univ_ids
                        year = year_grads
                        spec = specialities
                    else:
                        idTedu = tedu_ids[i]
                        idUniv = univ_ids[i]
                        year = year_grads[i]
                        spec = specialities[i]

                    date = datetime.datetime.strptime(year, '%d.%m.%Y')
                    database_session.add(Education(id_univ = idUniv, 
                    id_tedu = idTedu, year_grad = date, specialty = spec, id_empl = user_id))
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
                    database_session.add(EduLang(id_lang = langId, id_llev = llevId, id_empl = user_id))
                    i+=1           
                database_session.commit()
            
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def eduInfo(self):
        user_id = cherrypy.session.get('user_id')
        num_edu = 0
        num_lang = 0        
        with self.__database.session() as database_session:
            userfk = {'id_univ':[], 'id_tedu':[], 'year_grad':[], 'specialty':[], 'id_lang':[], 'id_llev':[]}

            for instance in database_session.query(Education).filter(Education.id_empl == user_id):
                userfk['id_univ'].append(instance.id_univ-1)
                userfk['id_tedu'].append(instance.id_tedu-1)
                userfk['year_grad'].append(str(instance.year_grad.strftime("%d.%m.%Y")))
                userfk['specialty'].append(instance.specialty)      
                num_edu = num_edu + 1
            
            for instance in database_session.query(EduLang).filter(EduLang.id_empl == user_id):
                userfk['id_lang'].append(instance.id_lang-1)
                userfk['id_llev'].append(instance.id_llev-1)
                num_lang = num_lang + 1
      
                
        result  =  {
                    'num_edu':num_edu,
                    'num_lang':num_lang
                    }         

        if(num_edu > 0):
            result['year_grad'] = userfk['year_grad']
            result['specialty'] = userfk['specialty']
            result['id_univ'] = userfk['id_univ']
            result['id_tedu'] = userfk['id_tedu']
        else:
            result['year_grad'] = ''
            result['specialty'] = ''
            result['id_univ'] = 0
            result['id_tedu'] = 0

        if(num_lang > 0):
            result['id_lang'] = userfk['id_lang']
            result['id_llev'] = userfk['id_llev']     
        else:
            result['id_lang'] = 0
            result['id_llev'] = 0 
        return result


