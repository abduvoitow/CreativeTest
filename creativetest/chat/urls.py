from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('chat/', views.chat_view, name='chat'),
    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('logout/', views.logout_view, name='logout'),
]
