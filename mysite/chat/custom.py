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
       
def load(code, username_):
    meet = Meet.objects.filter(code=code).first()
    retlist = []
    if meet:
        if meet.messages:
            msgdict = json.loads(meet.messages)
            for key,val in msgdict.items():
                dt = datetime.datetime.fromtimestamp(float(str(key)))
                username = val[0]
                message = val[1]
                retlist.append(
                    {
                        'message': message,
                        'username': username,
                        'dt': f"{dt.strftime('%I')}:{dt.strftime('%M')} {dt.strftime('%p')}",
                        #'admin': '#ffff80' if self.scope['user'].groups.filter(name='miniadmin').exists() else ''
                        'sender': ['justify-content-end','msg1'] if username_ == username else []
                    }
                )
    return retlist
                
        
