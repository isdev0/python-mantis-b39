import poplib
import email
import time
import quopri
from io import BytesIO


class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail_by_subject(self, username, password, subject):
        for i in range(10):
            pop = poplib.POP3(self.app.config['srv_email']['host'])
            pop.user(username)
            pop.pass_(password)
            email_count = pop.stat()[0]
            if email_count > 0:
                for i in range(email_count):
                    msglines = pop.retr(i+1)[1]
                    msgtext = "\n".join(map(lambda x: self.decode_quoted(x), msglines))
                    msg = email.message_from_string(msgtext)
                    if msg.get("Subject") == subject:
                        pop.dele(i+1)
                        pop.quit()
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None

    def decode_quoted(self, text):
        if type(text) is bytes:
            outputFile = BytesIO()
            inputFile = BytesIO(text)
            quopri.decode(inputFile, outputFile)
            return outputFile.getvalue().decode('utf-8')
        else: return text.decode('utf-8')
