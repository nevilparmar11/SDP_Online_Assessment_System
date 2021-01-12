from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

'''
Function to show homepage of the site
'''


def index(request):
    return render(request, 'index.html')


'''
Function to authenticate a user.
'''


def loginUser(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/users/home')
        else:
            return render(request, "users/login.html",
                          {
                              "errorMessage": "Invalid Credentials",
                              "username": username,
                              "password": password
                          }
                          )


'''
Function to redirect user to home page
'''


def home(request):
    if request.user.isStudent:
        return render(request, 'users/studentDashboard.html')
    else:
        return render(request, 'users/facultyDashboard.html')

'''
Function to Logout user
'''
def logoutUser(request):
    logout(request)
    return redirect('/users/login')