from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room/create/', views.create_room, name='create_room'),
    path('room/<slug:slug>/', views.room_detail, name='room_detail'),
    path('room/<slug:slug>/delete/', views.delete_room, name='delete_room'),
    path('room/<slug:slug>/invite/', views.create_room_invite, name='create_room_invite'),
    path('room/<slug:slug>/messages/', views.get_messages, name='get_messages'),
    path('room/<slug:slug>/send/', views.send_message, name='send_message'),
    path('profile/', views.profile, name='profile'),
    path('profile/add-integration/', views.add_ai_integration, name='add_ai_integration'),
    path('profile/subscribe/', views.create_yookassa_subscription, name='create_yookassa_subscription'),
    path('profile/confirm-subscription/', views.confirm_subscription, name='subscription_confirm'),
]
