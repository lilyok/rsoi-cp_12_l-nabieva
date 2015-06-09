# -*- coding: utf_8 -*-
import datetime
import os
import sys

from database import Database, Position, Industry, LangLevel, Lang, Universities, Schedule, IsTrip, Education, EduLang

def fill_database(database):
    with database.session() as database_session:        
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
                inds=inds+[Industry(name=line.decode(locale).strip())]        

        pos = [Position(name = u'java-developer', 
                        id_inds = '7', 
                        id_schd = '1', 
                        id_trip = '2', 
                        min_wage = '25000',
                        max_wage = '70000',
                        info = u'swing, spring, maven',
                        experience = '2.5'),
                Position(name = u'главный повар', 
                        id_inds = '15', 
                        id_schd = '2', 
                        id_trip = '1', 
                        min_wage = '30000',
                        max_wage = '50000',
                        info = u'классическое меню, небольшой штат сотрудников',
                        experience = '3')]   

        elan = [EduLang(id_lang = '1', id_llev = '2', id_pos = '1')]
        educ = [Education(id_univ = '94', specialty = u'программное обеспечение', id_pos = '1'),
                Education(id_univ = '99', specialty = u'технология производства', id_pos = '2')]
        database_session.add_all(llev)
        database_session.add_all(lang)
        database_session.add_all(trip) 
        database_session.add_all(inds)         
        database_session.add_all(schd)    
        database_session.add_all(univ)
        database_session.add_all(pos)    
        database_session.add_all(elan)  
        database_session.add_all(educ)                
       
# совершаем транзакцию       
        database_session.commit()
        
# посмотрим что уже есть в базе данных
    for instance in database_session.query(Lang).order_by(Lang.id):
        print instance

		
if __name__ == '__main__':
    filename='cdb.db'
    if os.path.exists(filename):
        os.remove(filename)

    database = Database('sqlite:///' + filename)
    database.create_tables()
    fill_database(database)