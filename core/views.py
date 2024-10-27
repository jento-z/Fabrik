from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile



# Create your views here.

@login_required(login_url='signin')
def index(request):
    #return HttpResponse('<h1>Welcome To Social Book</h1>')
    
    return render(request, 'index.html')

def settings(request):
    return render(request, 'setting.html')

def signup(request):
    
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #Log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
    else:        
        return render(request, 'signup.html')
    
<<<<<<< Updated upstream
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
=======
# def profile(request, pk):
#     user_object = User.objects.get(username=pk)
#     user_profile = Profile.objects.get(user=user_object)
#     user_posts = Posts.objects.filter(user=pk)
#     user_post_length = 

#     context = [
#         'user_object': user_object,
#         'user_profile': user_profile,
#     ]

#     return render(request, 'profile.html')
>>>>>>> Stashed changes
