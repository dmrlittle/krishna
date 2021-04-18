import json, datetime
from chat.models import Meet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def save(code, usrname, msg, dt, datatype):
    meet = Meet.objects.filter(code=code).first()
    if meet:
        if meet.messages:
            msgdict = json.loads(meet.messages)
        else:
            msgdict = {}            
        msgdict[datetime.datetime.timestamp(dt)] = [usrname, msg, datatype]
        meet.messages = json.dumps(msgdict)
        meet.save()

def send(room_id, msg, usr):
    channel_layer = get_channel_layer()
    dt = datetime.datetime.now()
    async_to_sync(channel_layer.group_send)(
                'chat_'+room_id,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'datatype': 'file',
                    'username': usr,
                    'dt': f"{dt.strftime('%I')}:{dt.strftime('%M')} {dt.strftime('%p')}",
                }
            )
    save(room_id,usr,msg,dt,'file')

    
def load(code, username_, ts):
    meet = Meet.objects.filter(code=code).first()
    retlist = []
    if meet:
        if meet.messages:
            msgdict = json.loads(meet.messages)
            for key,val in msgdict.items():
                if ts and float(str(key))<float(ts):
                    continue
                dt = datetime.datetime.fromtimestamp(float(str(key)))
                username = val[0]
                message = val[1]
                datatype = val[2]
                retlist.append(
                    {
                        'message': message,
                        'username': username,
                        'dt': f"{dt.strftime('%I')}:{dt.strftime('%M')} {dt.strftime('%p')}",
                        'datatype': datatype,
                        #'admin': '#ffff80' if self.scope['user'].groups.filter(name='miniadmin').exists() else ''
                        'sender': ['justify-content-end','msg1'] if username_ == username else []
                    }
                )
    return retlist
                
        
