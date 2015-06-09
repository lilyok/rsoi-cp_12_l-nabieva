from datetime import datetime
import email
import json

from mail_thread import MailThread


class MailParserThread(MailThread):

    def __init__(self, database, *args, **kwargs):
        self.__database = database
        MailThread.__init__(self, *args, **kwargs)

    def _process_message(self, message):
        _, sender = email.utils.parseaddr(message['from'])
        content = json.loads(message.get_payload())
        self.__process_parsed_message(sender, content)

    def __process_parsed_message(self, sender, content):
        pass
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