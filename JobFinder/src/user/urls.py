from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
        path('signup/',views.signup , name='signup'),
        path('profile/', views.profile, name='profile'),
        path("verify_email/", views.verify_email, name="verify_email"),
        

]