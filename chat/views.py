from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import RegisterForm
from .models import Message, Profile

@login_required(login_url='chat:login')
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