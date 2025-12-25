from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('chat/', views.chat_view, name='chat'),
    path('api/get-new-messages/', views.get_new_messages, name='get_new_messages'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('logout/', views.logout_view, name='logout'),
]
