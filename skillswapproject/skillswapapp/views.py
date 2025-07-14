from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Skill
from .forms import SkillForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserForm, UserProfileForm
from skillswapapp import models  # for login session
from django.db.models import Q
from .forms import CustomSignupForm

def index(request):
    return render(request, "skillswapapp/index.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember = request.POST.get("remember")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # records available in session
            request.session["username"] = user.username
            request.session["email"] = user.email
            request.session["fullname"] = user.first_name

            if not remember:
                # Session will expire when the browser is closed
                request.session.set_expiry(0)
            else:
                # Session will expire in 2 weeks (default)
                request.session.set_expiry(1209600)

            return redirect("skillswapapp:skills")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("skillswapapp:login")

    return render(request, "skillswapapp/login.html")


def user_logout(request):
    logout(request)
    return redirect("skillswapapp:login")

def register(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('skillswapapp:index')  
    else:
        form = CustomSignupForm()
    return render(request, 'skillswapapp/register.html', {'form': form})




@login_required(login_url="skillswapapp:login")
def skills(request):
    query = request.GET.get("q", "")
    current_username = request.session.get("username")

    skills = Skill.objects.exclude(user__username=current_username)

    if query:
        skills = skills.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "skillswapapp/skills.html", {"skills": skills})


@login_required(login_url="skillswapapp:login")
def addskills(request):
    return render(request, "skillswapapp/addskills.html")


@login_required(login_url="skillswapapp:login")
def skilldetails(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    return render(request, "skillswapapp/skilldetails.html", {"skill": skill})


@login_required(login_url="skillswapapp:login")
def profile(request):
    user_skills = request.user.skills.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('skillswapapp:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, "skillswapapp/profile.html", {
        "user_skills": user_skills,
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
    })

@login_required(login_url="skillswapapp:login")
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_skills = Skill.objects.filter(user=user)

    return render(request, 'skillswapapp/view_profile.html', {
        'viewed_user': user,
        'user_profile': user_profile,
        'user_skills': user_skills,
    })


@login_required(login_url="skillswapapp:login")
def deleteskill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    skill.delete()
    return redirect("skillswapapp:profile")


@login_required(login_url="skillswapapp:login")
def addskills(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect("skillswapapp:skills")
    else:
        form = SkillForm()
    return render(request, "skillswapapp/addskills.html", {"form": form})


# def review(request): # optional
#     return render(request, 'skillswapapp/review.html')


def contact_user_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if message:
            return render(request, 'skillswapapp/contact.html', {
                'skill': skill,
                'success': True,
                'message': message
            })
        else:
            return render(request, 'skillswapapp/contact.html', {
                'skill': skill,
                'error': "Message cannot be empty."
            })

    return render(request, 'skillswapapp/contact.html', {'skill': skill})

