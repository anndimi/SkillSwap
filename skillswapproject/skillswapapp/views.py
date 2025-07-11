from django.shortcuts import render

def index(request):
    return render(request, 'skillswapapp/index.html')

def user_login(request):
    return render(request, 'skillswapapp/login.html')

def register(request):
    return render(request, 'skillswapapp/register.html')

def skills(request):
    return render(request, 'skillswapapp/skills.html')

def addskills(request):
    return render(request, 'skillswapapp/addskills.html')

def skilldetails(request):
    return render(request, 'skillswapapp/skilldetails.html')

# def review(request): # optional
#     return render(request, 'skillswapapp/review.html')

# def contact(request):  # optional
#     return render(request, 'skillswapapp/contact.html')

