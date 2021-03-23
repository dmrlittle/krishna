import json, datetime
from chat.models import Meet


def save(code, usrname, msg, dt):
    meet = Meet.objects.filter(code=code).first()
    if meet:
        if meet.messages:
            msgdict = json.loads(meet.messages)
        else:
            msgdict = {}            
        msgdict[datetime.datetime.timestamp(dt)] = [usrname, msg]
        meet.messages = json.dumps(msgdict)
        meet.save()
       
        
