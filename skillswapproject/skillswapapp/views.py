from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required # for login session

def index(request):
    return render(request, 'skillswapapp/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # records available in session
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['fullname'] = user.first_name

            if not remember:
                # Session will expire when the browser is closed
                request.session.set_expiry(0)
            else:
                # Session will expire in 2 weeks (default)
                request.session.set_expiry(1209600)

            return redirect('skillswapapp:skills')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('skillswapapp:login')

    return render(request, 'skillswapapp/login.html')

def user_logout(request):
    logout(request)
    return redirect('skillswapapp:login')


def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('skillswapapp:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('skillswapapp:register')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fullname
            )
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('skillswapapp:login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('skillswapapp:register')

    return render(request, 'skillswapapp/register.html')


@login_required(login_url='skillswapapp:login')
def skills(request):
    return render(request, 'skillswapapp/skills.html')

@login_required(login_url='skillswapapp:login')
def addskills(request):
    return render(request, 'skillswapapp/addskills.html')

@login_required(login_url='skillswapapp:login')
def skilldetails(request):
    return render(request, 'skillswapapp/skilldetails.html')

@login_required(login_url='skillswapapp:login')
def profile(request):
    return render(request, 'skillswapapp/profile.html')

# def review(request): # optional
#     return render(request, 'skillswapapp/review.html')

# def contact(request):  # optional
#     return render(request, 'skillswapapp/contact.html')



