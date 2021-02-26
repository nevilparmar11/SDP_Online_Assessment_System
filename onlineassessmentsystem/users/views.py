from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from users.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError

from users.decorators import faculty_required
import pandas as pd
from datetime import datetime

# To encode a login redirect message string into query string parameter
loginRedirectMessage = urlencode({'msg': 'Please Login'})

'''
Function to show homepage of the site
'''


def index(request):
    return render(request, 'index.html', {'year': str(datetime.now().year)})


'''
    Function to register Students
'''


@faculty_required()
def registerStudents(request):
    if request.method == "GET":
        return render(request, 'users/registerStudents.html')

    else:
        try:
            inputFile = request.FILES['inputFile']
        except MultiValueDictKeyError:
            return render(request, 'users/registerStudents.html', {"errorMessage": "File is not selected"})

        data = pd.read_excel(inputFile, index_col=0)
        row = data.shape[0]
        msg = ""
        for i in range(row):
            firstName = data.iloc[i][0]
            lastName = data.iloc[i][1]
            email = data.iloc[i][2]
            username = data.iloc[i][3]
            password = data.iloc[i][4]
            if User.objects.filter(username=username).exists():
                msg += "ERROR : " + "Username : " + username + " for " + firstName + " " + lastName + " is already exist.\n"
            else:
                user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, password=password, email=email)
                user.is_active = True
                user.save()
                msg += "SUCCESS : " + firstName + " " + lastName + " with Username : " + username + " is registered successfully.\n"

        return render(request, 'users/registerStudents.html', {'msg': msg})


'''
Function to authenticate a user.
'''


def loginUser(request):
    if request.method == "GET":
        data = {}
        msg = request.GET.get('msg')
        if msg is not None:
            data["errorMessage"] = msg
        nextUrl = request.GET.get('next')
        if nextUrl is not None:
            data["next"] = nextUrl
        return render(request, "users/login.html", data)
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['userId'] = user.id
            request.session['userName'] = username
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            if user.isStudent:
                request.session['role'] = 'student'
            else:
                request.session['role'] = 'faculty'
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


@login_required(login_url='/users/login?' + loginRedirectMessage)
def home(request):
    return redirect("/classroom")


'''
Function to Logout user
'''


def logoutUser(request):
    logout(request)
    return redirect('/users/login')


'''
Function to redirect user to custom 404 Error Page 
'''


def pageNotFound(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


'''
Function to redirect user to custom 404 Error Page 
'''


def internalServerError(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def accessDemied(request):
    return render(request, 'accessDenied.html')


'''Function To display user profile page'''


@login_required(login_url='/users/login?' + loginRedirectMessage)
def viewProfile(request):
    return render(request, 'users/profile.html')


'''Function To edit user's details'''


@login_required(login_url='/users/login?' + loginRedirectMessage)
def editProfile(request):
    if request.method == "GET":
        return render(request, '404.html')
    username = request.POST.get("username")
    firstName = request.POST.get("firstName")
    lastName = request.POST.get("lastName")
    email = request.POST.get("email")
    try:
        profilePic = request.FILES['profilePic']
    except MultiValueDictKeyError:
        profilePic = None

    user = request.user
    oldUsername = user.username
    try:
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.username = username
        if profilePic is not None:
            user.profilePicture.delete(save=False)
            user.profilePicture = profilePic
        user.save()
        return redirect('/users/viewProfile')
    except IntegrityError:
        user.username = oldUsername
        return render(request, 'users/profile.html', {"errorMessage": "Username is already taken"})


def changePassword(request):
    oldPassword = request.POST.get("oldPassword")
    user = authenticate(username=request.user.username, password=oldPassword)
    if user is None:
        return render(request, 'users/profile.html', {"pwdErrorMessage": "Incorrect Old Password"})
    newPassword = request.POST.get("password")
    user.set_password(newPassword)
    user.save()
    login(request, user)
    return redirect("/users/viewProfile")
