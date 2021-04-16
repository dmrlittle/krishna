from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserProfile
from chat.models import Meet
from chat.forms import MeetForm
from django.contrib import messages
from chat.custom import load
from django.http import Http404

@login_required
def chat(request, room_id=None):
    if request.method == 'POST':
        form1 = MeetForm(request.POST)
        if form1.is_valid():
            room_id = form1.cleaned_data['code']
            if not Meet.objects.filter(code=room_id).first():
                meet = Meet(code=room_id)
                meet.save()
                user = UserProfile.objects.filter(user = request.user).first()
                meet.members.add(user)
                meet.admin.add(user)
                return redirect('chat:pilot')
        else:
            if request.POST.getlist('add_mem',None):
                meet = Meet.objects.filter(code=request.POST.get('meet_code',None)).first()
                users = UserProfile.objects.filter(id__in = request.POST.getlist('add_mem',None))
                [meet.members.add(user) for user in users if meet]
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
    room_id = room_id if room_id else (UP.groups.all()[0].code if UP.groups.all() else '')
    meet_ = Meet.objects.filter(code=room_id).first()
    if Meet.objects.filter(code=room_id).first():
        members = Meet.objects.filter(code=room_id).first().members.all()
    else:
        members=[]

    nonmembers = set(UserProfile.objects.all()) - set(members)
    context = {'room_id':room_id,'admin':(True if meet_ and meet_.admin.all()[0].user.username == user.username else False), 'UP':UP ,'username':user.username, 'meets':meets,'form':form, 'nonmembers':nonmembers, 'members':members, 'msglist':load(room_id, user.username)}

    return render(request, 'chat/chat.html', context)

@login_required
def pilot(request):
    if request.method == 'POST':
        form = MeetForm(request.POST)
        if form.is_valid():
            room_id = form.cleaned_data['code']
            if request.POST['type'] == 'create' and request.user.groups.filter(name='miniadmin').exists():
                meet = Meet(code=room_id)
                meet.save()
                return redirect('chat:chat', room_id=room_id)
            elif request.POST['type'] == 'join':
                meet = Meet.objects.filter(code=room_id).first()
                if meet:
                    return redirect('chat:chat', room_id=room_id)
                else:
                    messages.error(request, "Invalid Code: The given meet code is invalid or has expired !")
                    form = MeetForm()
    else:
        form = MeetForm()
        
    context={'form':form}
    return render(request, 'chat/pilot.html', context)
