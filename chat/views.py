from django.core.checks import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

from .forms import RegisterForm
from .models import Message, Profile


def index(request):
    try:
        friends = Profile.objects.get(user_id = request.user.id ).friends.all()
    except:
        friends=None
    context = {'friends':friends}
    return render(request, 'chat/index.html',context )

@login_required(login_url='chat:login')
def getMessages(request,pk):
    user = Profile.objects.get(user_id = request.user.id)
    messages = user.getMessages(pk)
    return JsonResponse(messages, safe=False)

class RegisterView(CreateView):
    template_name = 'chat/signup.html'
    model = User
    form_class = RegisterForm
    success_url ='/'

