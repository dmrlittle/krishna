from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Meet
from chat.forms import MeetForm
from django.contrib import messages

@login_required
def chat(request, room_id):
    user = request.user
    context = {'room_id':room_id, 'username':user.username}
    return render(request, 'chat/chat1.html', context)

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
