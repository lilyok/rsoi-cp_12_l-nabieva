from datetime import datetime
import email
import json
from mail_thread import MailThread
from database import Positions

class MailParserThread(MailThread):


    def __init__(self, database, *args, **kwargs):
        self.__database = database
        MailThread.__init__(self, *args, **kwargs)
 
    def _process_message(self, message):
        print "_process_message"
        _, sender = email.utils.parseaddr(message['from'])
        content = json.loads(message.get_payload())
        self.__process_parsed_message(sender, content)

    def __process_parsed_message(self, sender, content):
        print "__process_parsed_message"
        with self.__database.session() as database_session:    
            for pos in content:    
                print float(pos['status'])
                if(float(pos['status']) > 0):

                    cur_lan = ""
                    cur_edu = ""
                    for lan in pos['lan']:
                        cur_lan += lan+"; "
                    for educ in pos['educ']:
                        cur_edu += educ+"; "

                    try:
                        expos = database_session.query(Positions).filter(Positions.id_pos == pos['id']).filter(Positions.e_mail == sender).filter(Positions.id_empl == pos['eid']).one()
                        expos.name = pos['name']
                        expos.info = pos['info']
                        expos.schd = pos['schd']
                        expos.trip = pos['trip']
                        expos.min_wage = pos['min_wage']
                        expos.max_wage = pos['max_wage']
                        expos.experience = pos['experience']
                        expos.lan = cur_lan
                        expos.educ = cur_edu
                        expos.status = pos['status']
                        database_session.add(expos)
                    except Exception, e:
                        database_session.add(Positions(id_pos = pos['id'], name = pos['name'], info = pos['info'], 
                            schd = pos['schd'], trip = pos['trip'], min_wage = pos['min_wage'], max_wage = pos['max_wage'],
                            experience = pos['experience'], lan = cur_lan, educ = cur_edu, e_mail = sender, id_empl = pos['eid'], status = pos['status']))
                else:
                    try:
                        expos = database_session.query(Positions).filter(Positions.id_pos == pos['id']).filter(Positions.e_mail == sender).filter(Positions.id_empl == pos['eid']).one()
                        if expos.status != -5:
                            expos.status = pos['status']
                        # database_session.delete(expos)
                    except Exception, e:
                        print e
  


         # pass
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