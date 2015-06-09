from datetime import datetime
import email
import json

from mail_thread import MailThread
from database import Resume


class MailParserThread(MailThread):

    def __init__(self, database, *args, **kwargs):
        print "__init__"
        self.__database = database
        MailThread.__init__(self, *args, **kwargs)

    def _process_message(self, message):
        print "_process_message"
        _, sender = email.utils.parseaddr(message['from'])
        content = json.loads(message.get_payload())
        self.__process_parsed_message(sender, content)

    def __process_parsed_message(self, sender, content):
        print "__process_parsed_message"
        print sender
        print content['email']
        with self.__database.session() as database_session:  
            if(float(content['status']) != 0):  
                cur_lan = ""
                cur_edu = ""

                for lan in content['lan']:
                    cur_lan += lan+"; "
                for educ in content['educ']:
                    cur_edu += educ+"; "
                try:
                    exres = database_session.query(Resume).filter(Resume.resm_id == content['id']).filter(Resume.e_mail == sender).filter(Resume.id_pos == content['id_pos']).one()
                    exres.name = content['name']
                    exres.post = content['post']
                    exres.skills = content['skills']
                    exres.schd = content['schd']
                    exres.trip = content['trip']
                    exres.wage = content['wage']
                    exres.exp = content['exp']
                    exres.lan = cur_lan
                    exres.educ = cur_edu
                    exres.status = content['status']
                    if content['email']:
                        exres.email = content['email']
                    database_session.add(exres)
                except Exception, e:
                    database_session.add(Resume(resm_id = content['id'], name = content['name'], post = content['post'], 
                        schd = content['schd'], trip = content['trip'], wage = content['wage'], skills = content['skills'],
                        exp = content['exp'], lan = cur_lan, educ = cur_edu, e_mail = sender, id_pos = content['id_pos'], status = content['status'],email = content['email']))

            else:
                try:
                    exres = database_session.query(Resume).filter(Resume.resm_id == content['id']).filter(Resume.e_mail == sender).filter(Resume.id_pos == content['id_pos']).one()
                    exres.status = content['status']
                    # database_session.delete(expos)
                except Exception, e:
                    print e  
        # uuid = content['uuid']
        # state = content['state']

        # with self.__database.session() as database_session:

        #     reservation = database_session.query(Reservation).\
        #         filter_by(uuid=uuid).one()

        #     if state == 'reserved':
        #         reservation.status = Reservation.STATUS_RESERVED
        #     elif state == 'denied':
        #         reservation.status = Reservation.STATUS_DENIED
        #     elif state == 'cancelled':
        #         reservation.status = Reservation.STATUS_CANCELLED