from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .import views

app_name = 'chat'
urlpatterns = [
    path('', views.index, name= 'home'),
    path('getMessages/<str:pk>/', views.getMessages, name='getMessages'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name="chat/logout.html"), name='logout')
]
