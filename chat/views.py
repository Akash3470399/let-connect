import json
from django.core.checks import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings

from .forms import RegisterForm, SignInForm
from .models import Message, CustomUser

@login_required(login_url='chat:login')
def index(request):
    try:
        friends = request.user.friends.all()
    except:
        friends=None
    context = {'friends':friends}
    return render(request, 'chat/index.html',context )

@login_required(login_url='chat:login')
def getMessages(request,pk):
    messages = Message.getMessages(request.user.id, pk)
    return JsonResponse(messages, safe=False)

@login_required(login_url='chat:login')
def getUsersList(request):
    try:
        users = CustomUser.objects.all()
        usersList = []
        for user in users:
            if user == request.user or (user in request.user.friends.all()):
                continue
            u = {
                'username':user.name,
                'email':user.email,
            }
            usersList.append(u)
    except:
        usersList = None
    
    return JsonResponse(usersList, safe=False)

@login_required(login_url="chat:login")
def add_friend(request):
    user_email = json.load(request)['name']
    try:
        request.user.friends.add(CustomUser.objects.get(email = user_email))
        friend = request.user.friends.get(email = user_email)
        data = {'id':friend.id, 'name':friend.name}
    except:
        data = None
    return JsonResponse(data, safe=False)

class RegisterView(CreateView):
    template_name = 'chat/signup.html'
    model = settings.AUTH_USER_MODEL
    form_class = RegisterForm
    success_url ='/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_errors = []
        try:
            errors = eval(context['form'].errors.as_json())
            for value in errors.values():
                my_errors.append(value[0]['message'])
        except:
            pass
        context['form_errors'] = my_errors
        return context
    
class CustomLoginView(UserPassesTestMixin,LoginView):
    template_name='chat/login.html'
    # form_class = SignInForm
    # authentication_form = SignInForm

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        try:
            form_error = eval(context['form'].errors.as_json())
            my_error = form_error['__all__'][0]['message']
            context['form_errors'] = my_error
        except:
            pass
        return context

    def test_func(self):
        return not self.request.user.is_authenticated

class CustomLogoutView(LogoutView):
    template_name = 'chat/logout.html'