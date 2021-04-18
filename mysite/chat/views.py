from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import UserProfile
from chat.models import Meet, File
from chat.forms import MeetForm, FileForm
from django.contrib import messages
from chat.custom import load, send
from django.http import Http404
import os, json, datetime

@login_required
def chat(request, room_id=None):
    if not UserProfile.objects.filter(user=request.user.id).first():
        raise Http404('Only Users registered via signup allowed!')
    if request.method == 'POST':
        form1 = MeetForm(request.POST)
        fileform = FileForm(request.POST, request.FILES)
        if form1.is_valid():
            room_id = form1.cleaned_data['code']
            if not Meet.objects.filter(code=room_id).first():
                meet = Meet(code=room_id)
                meet.save()
                user = UserProfile.objects.filter(user = request.user).first()
                meet.members.add(user)
                meet.admin.add(user)
                if meet.membermeta:
                    mm = json.loads(meet.membermeta)
                else:
                    mm = {}
                mm[str(user.user.id)]= datetime.datetime.timestamp(datetime.datetime.now())
                meet.membermeta = json.dumps(mm)
                meet.save()
                return redirect('chat:pilot')
        elif fileform.is_valid():
            file = File(file = request.FILES['file'])
            file.save()
            send(request.POST.get('meet_code',None), [os.path.basename(file.file.name),request.META['HTTP_HOST']+file.file.url], request.user.username)
            if request.POST.get('meet_code',None) and request.POST.get('meet_code',None)!='' :
                return (redirect('chat:chat', room_id=request.POST.get('meet_code',None))) 
            else:
                return redirect('chat:pilot')
        else:
            if request.POST.getlist('add_mem',None):
                meet = Meet.objects.filter(code=request.POST.get('meet_code',None)).first()
                users = UserProfile.objects.filter(id__in = request.POST.getlist('add_mem',None))
                [meet.invited.add(user) for user in users if meet]
                return redirect('chat:pilot')
            elif request.POST.getlist('remove_mem',None):
                meet = Meet.objects.filter(code=request.POST.get('meet_code',None)).first()
                users = UserProfile.objects.filter(id__in = request.POST.getlist('remove_mem',None))
                [meet.members.remove(user) for user in users if meet]
                return redirect('chat:pilot')
            elif request.POST.get('leave_grp',None) == '1':
                meet = Meet.objects.filter(code=request.POST.get('meet_code',None)).first()
                users = UserProfile.objects.filter(user=request.user.id)
                [meet.members.remove(user) for user in users if meet]
                return redirect('chat:pilot')
            elif request.POST.get('delete_grp',None) == '1':
                meet = Meet.objects.filter(code=request.POST.get('meet_code',None)).first()
                meet.delete()
                return redirect('chat:pilot')
            elif request.POST.getlist('invite_res',None):
                meets = Meet.objects.filter(id__in=request.POST.getlist('meet_code',None))
                user = UserProfile.objects.filter(user = request.user).first()
                if request.POST.get('submit',None) == 'accept' :
                    [meet.members.add(user) for meet in meets if meet]
                    for meet in meets:
                        if meet.membermeta:
                            mm = json.loads(meet.membermeta)
                        else:
                            mm = {}
                        mm[str(user.user.id)]= datetime.datetime.timestamp(datetime.datetime.now())
                        meet.membermeta = json.dumps(mm)
                        meet.save()
                elif request.POST.get('submit',None) == 'decline' :
                    pass                
                [meet.invited.remove(user) for meet in meets if meet]
                return redirect('chat:pilot')
            
    if room_id != None:
        meet = Meet.objects.filter(code=room_id).first()
        if meet:
            if UserProfile.objects.filter(user=request.user.id).first() not in meet.members.all():
                raise Http404("Page does not exist")
        else:
            raise Http404("Page does not exist")
    user= request.user
    UP = UserProfile.objects.filter(user=request.user.id).first()
    meets = Meet.objects.all()
    
    form = MeetForm()
    fileform = FileForm()
    room_id = room_id if room_id else (UP.groups.all()[0].code if UP.groups.all() else '')
    meet_ = Meet.objects.filter(code=room_id).first()
    if Meet.objects.filter(code=room_id).first():
        members = Meet.objects.filter(code=room_id).first().members.all()
        invited = Meet.objects.filter(code=room_id).first().invited.all()
    else:
        members=[]
        invited=[]
    
    def userjointime():
        if meet_ and meet_.membermeta:
            jt = float(json.loads(meet_.membermeta).get(str(request.user.id),0.0))
        else:
            jt = 0.0
        return jt
    
    nonmembers = set(UserProfile.objects.all()) - set(members) - set(invited)
    context = {'room_id':room_id,'admin':(meet_.admin.all()[0].user.username if meet_ else False), 
               'UP':UP ,'username':user.username, 'meets':meets,'form':form,'fileform':fileform, 
               'nonmembers':nonmembers, 'members':members, 'invited':invited,
               'msglist':load(room_id, user.username, userjointime())}

    return render(request, 'chat/chat.html', context)

