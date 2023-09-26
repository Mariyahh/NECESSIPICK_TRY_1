from datetime import date
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm
from django.core.files import File 
from .models import MongoDBUser

# Create your views here.
def HomePage(request):
    return render(request, 'home/index.html', {})

def Register(request):
    if request.method == 'POST':
        # account
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # personal information
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        # age = request.POST.get('age')
        purpose = request.POST.get('purpose')

        # Calculate age
        today = date.today()
        birth_date = date.fromisoformat(birthday)
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # saving into database
        new_user = User.objects.create_user(uname, email, password)
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.save()

        # Create a UserProfile model (assuming you have one) to store additional user information
        user_profile = UserProfile(user=new_user, gender=gender, birthday=birthday, age=age, purpose=purpose)

        # Set the default profile picture for the user profile
        # First, you need to open the default profile picture file and assign it to the profile_picture field.
        with open('media/profile_pics/default_profile.png', 'rb') as f:
            default_profile_picture = File(f)
            user_profile.profile_picture.save('default_profile.png', default_profile_picture, save=True)

        user_profile.save()

        return redirect('login-page')
    return render(request, 'auth_system/register.html', {})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = ProfilePictureForm(instance=user_profile)  # Define the form here
    return render(request, 'auth_system/profile.html', {'user_profile': user_profile, 'form': form})

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=request.user.userprofile)
    
    return render(request, 'auth_system/update_profile_picture.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        # account
        username = request.POST.get('username')
        password = request.POST.get('passwordli')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back, {user.first_name} {user.last_name}')
            return redirect('auth_home')
        else:
            messages.error(request, 'Error, User does not Exist')

    return render(request, 'auth_system/login.html', {})



def Logout(request):
    logout(request)
    return redirect('login-page')