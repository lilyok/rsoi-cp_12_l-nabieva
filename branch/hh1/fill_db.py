# -*- coding: utf_8 -*-
import datetime
import os
import sys

from database import Database, Empl, TypeOfEdu, LangLevel, Lang, Universities, Industry, Schedule, IsTrip, Resume

def fill_database(database):
    with database.session() as database_session:
           
        empls = [Empl(name=u'Лилия', 
                      surname=u'Набиева',
                      thirdname=u'Ильдусовна',
                      birthday=datetime.date(1989,05,26),
                      email=u'lilly666@list.ru',
                      password=u'666'),
                 Empl(name=u'Василь', 
                      surname=u'Иванов',
                      thirdname=u'Александрович',
                      birthday=datetime.date(1989,10,02),
                      email=u'master@vasil.ru',
                      password=u'123')]   
                      
        tedus = [TypeOfEdu(name=u'неоконченное высшее'), 
                 TypeOfEdu(name=u'незаконченное высшее'), 
                 TypeOfEdu(name=u'высшее'), 
                 TypeOfEdu(name=u'аспирантура')] 
                 
        llev = [LangLevel(name=u'читаю со словарем'), 
                LangLevel(name=u'читаю-перевожу профессиональную литературу'), 
                LangLevel(name=u'хорошие разговорные навыки')]
                
        lang = [Lang(name=u'английский'), 
                Lang(name=u'немецкий'), 
                Lang(name=u'французский')]
                
        schd = [Schedule(name=u'полный день'),
                Schedule(name=u'сменный график'),
                Schedule(name=u'гибкий график'),
                Schedule(name=u'удаленная работа')]
                
        trip = [IsTrip(name=u'не готов'),
                IsTrip(name=u'иногда'),
                IsTrip(name=u'готов')]
                
        locale='utf8'
        univ=[]
        with open("for_db/univer_data.txt") as rows:
            for line in rows:
                print line
                univ=univ+[Universities(name=line.decode(locale).strip())]
        inds=[]
        with open("for_db/industry_data.txt") as rows:
            for line in rows:
                print line
                llist = line.decode(locale).strip().split(':')
                for el in llist:
                  print el.encode(locale)
                if len(llist) == 2:
                  inds=inds+[Industry(name=llist[0], e_mail=llist[1])]  
                else:
                  inds=inds+[Industry(name=llist[0])]             
        
        res = [Resume(id_inds=1, id_schd=1, id_trip=2, post=u'java-developer',  
               min_wage=100000, max_wage=200000, experience=1.5, 
               skills=u'java, maven, sql, svn', id_empl=2),
              Resume(id_inds=2, id_schd=3, id_trip=1, post=u'помощник бухгалтера',  
               min_wage=25000, max_wage=35000, experience=0.5, 
               skills=u'1с', id_empl=1),
              Resume(id_inds=3, id_schd=1, id_trip=2, post=u'юрконсультант',  
               min_wage=30000, max_wage=40000, experience=1.5, 
               skills=u'составление договоров и завещаний, оформление сделок', id_empl=1)]

        database_session.add_all(empls)
        database_session.add_all(tedus)
        database_session.add_all(llev)
        database_session.add_all(lang)
        database_session.add_all(trip) 
        database_session.add_all(inds)         
        database_session.add_all(schd)    
        database_session.add_all(univ)
        database_session.add_all(res)       
        
# совершаем транзакцию       
        database_session.commit()
        
# посмотрим что уже есть в базе данных
    for instance in database_session.query(Lang).order_by(Lang.id):
        print instance

		
if __name__ == '__main__':
    filename='hhdb.db'
    if os.path.exists(filename):
        os.remove(filename)

    database = Database('sqlite:///' + filename)
    database.create_tables()
    fill_database(database)