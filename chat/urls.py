from django.urls import path
from .import views

app_name = 'chat'
urlpatterns = [
    path('', views.index, name= 'home'),
    path('getMessages/<str:pk>/', views.getMessages, name='getMessages'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',views.CustomLoginView.as_view(), name='login'),
    path('logout/',views.CustomLogoutView.as_view(), name='logout'),
]
