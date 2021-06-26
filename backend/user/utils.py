from locowin.settings import EMAIL_HOST_USER
from django.core.mail import send_mail	
import datetime


class Util:
    @staticmethod
    def send_email(data):
        s = "Hi," + data['email_body']['username'] + ". " + data['email_body']['message'] + ". " + data['email_body']['link']
        send_mail(data['email_subject'],s,EMAIL_HOST_USER,[data['to_email']])
    @staticmethod
    def slot_send_email(data):
        data['email_body']['date'] = data['email_body']['date'] + datetime.timedelta(hours=5, minutes=30) 
        s = "Hi," + data['email_body']['username'] + ". " + data['email_body']['message'] + ". The waypoint is " + data['email_body']['waypoint'] + " at " + str(data['email_body']['date']) + " with the following brand " + data['email_body']['brand'] +". The dose number is " + str(data['email_body']['dose'])
        send_mail(data['email_subject'],s,EMAIL_HOST_USER,[data['to_email']]) 
        
    @staticmethod
    def send_confirmation(data):
        data['email_body']['date'] = data['email_body']['date'] + datetime.timedelta(hours=5, minutes=30) 
        s = "Hi," + data['email_body']['username'] + ". " + data['email_body']['message'] + ". The waypoint is " + data['email_body']['waypoint'] + " at " + str(data['email_body']['date']) + " with the following brand " + data['email_body']['brand'] + ". The dose number is " + str(data['email_body']['dose'])
        send_mail(data['email_subject'],s,EMAIL_HOST_USER,[data['to_email']]) 
        
    @staticmethod
    def send_cancellation(data):
        data['email_body']['date'] = data['email_body']['date'] + datetime.timedelta(hours=5, minutes=30) 
        s = "Hi," + data['email_body']['username'] + ". " + data['email_body']['message'] + ". The waypoint was " + data['email_body']['waypoint'] + " at " + str(data['email_body']['date']) + " with the following brand " + data['email_body']['brand'] +". The dose number was " + str(data['email_body']['dose'])
        send_mail(data['email_subject'],s,EMAIL_HOST_USER,[data['to_email']]) 
