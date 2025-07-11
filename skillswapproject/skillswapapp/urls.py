# File that includes all URLs required

from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = "skillswapapp"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="skillswapapp:index", permanent=False)),
    path("index/", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("skills/", views.skills, name="skills"),
    path("addskills/", views.addskills, name="addskills"),
    path("skilldetails/", views.skilldetails, name="skilldetails"),
    path("profile/", views.profile, name="profile"),
    path("profile/delete/<int:skill_id>/", views.deleteskill, name="deleteskill"),
    # path("review/", views.review, name="review"), #optional
    # path("contact/", views.contact, name="contact"),  #optional
]
