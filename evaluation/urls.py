from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('request_evaluation/', views.logout_user, name='logout'),
    path('logout/', views.logout_user, name='logout')
]
