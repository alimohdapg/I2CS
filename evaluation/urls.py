from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='evaluation_logout'),
    path('request_evaluation/', views.request_evaluation, name='request_evaluation'),
    path('evaluations/', views.evaluations, name='evaluations'),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate')
]
