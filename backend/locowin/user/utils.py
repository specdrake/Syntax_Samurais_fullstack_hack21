from locowin.settings import EMAIL_HOST_USER
from django.core.mail import send_mail	


class Util:
    @staticmethod
    def send_email(data):
        s = "Hi," + data['email_body']['username'] + ". " + data['email_body']['message'] + ". " + data['email_body']['link']
        send_mail(data['email_subject'],s,EMAIL_HOST_USER,[data['to_email']])