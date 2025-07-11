# File that includes all URLs required

from django.urls import path
from . import views

app_name = 'skillswapapp'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("skills/", views.skills, name="skills"),
    path("addskills/", views.addskills, name="addskills"),
    path("skilldetails/", views.skilldetails, name="skilldetails"),
    # path("review/", views.review, name="review"), #optional
    # path("contact/", views.contact, name="contact"),  #optional
]