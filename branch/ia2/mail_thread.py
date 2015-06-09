import email
import poplib
from threading import Event, Thread
import time
import traceback


class MailThread(Thread):

    __POP3_SERVER = 'dev.iu7.bmstu.ru'
    __POP3_SERVER_PORT = 10110
    __PASSWORD = 'MBZqz'
    __QUERY_INTERVAL = 5; # Seconds

    def __init__(self, mail_address):
        self._mail_address = mail_address
        self.__stopped = Event()
        Thread.__init__(self)

    def run(self):
        while not self.__stopped.isSet():

            time.sleep(self.__QUERY_INTERVAL)

            try:
                self.__mail_box =\
                    poplib.POP3(self.__POP3_SERVER, self.__POP3_SERVER_PORT)

            except poplib.error_proto:
                traceback.print_exc()
                continue

            self.__mail_box.user(self._mail_address)
            self.__mail_box.pass_(self.__PASSWORD)

            message_count, _ = self.__mail_box.stat()

            messages = []
            for message_index in xrange(message_count):
                message = email.message_from_string(
                    '\n'.join(self.__mail_box.retr(message_index + 1)[1]))
                messages.append(message)
                self.__mail_box.dele(message_index + 1)

            self.__mail_box.quit()

            for message in messages:
                try:
                    self._process_message(message)
                except Exception:
                    traceback.print_exc()

        print "Mail processing stopped"

    def stop(self):
        self.__stopped.set()

    def _process_message(self, message):
        raise NotImplementedError('')
