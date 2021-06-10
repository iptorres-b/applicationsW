from django.core.checks import messages
import users
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.utils import IntegrityError
from django.contrib import messages

#Views
from django.views import View

#Models
from django.contrib.auth.models import User
from users.models import Student, Teacher

# Create your views here.
def login_view(request):
    """ Login view """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('landing')
        else:
            try:
                user = User.objects.get(username=username)
                return render(request, 'users/login.html',{'error':'Invalid password'})
            except:
                return render(request, 'users/login.html',{'error':'Invalid username and password'})

    return render(request, 'users/login.html')

def signup(request):
    """ Sign up view """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['confirmpassword']

        if password != password_confirmation:
            return render(request, 'users/signup.html',{'error':'Password does not match'})

        try:
            if User.objects.get(email=request.POST['email']):
                return render(request,'users/signup.html', {'error':'Email has already taken'})
        except:
            pass

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return render(request, 'users/signup.html',{'error':'Username already taken'})

        user.first_name = request.POST['name']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.save()

        type_of_user = request.POST['type']

        if type_of_user == 'teacher':
            profile = Teacher(teacher=user)
        else:
            profile = Student(student=user)
            
        profile.save()

        messages.success(request, "The account was created with success")
        return redirect('login')

    return render(request,'users/signup.html')
    

@login_required
def landing(request):
    return render(request,'landing.html')


@login_required
def logout_view(request):
    """ Logout a user view """
    logout(request)
    return redirect('login')