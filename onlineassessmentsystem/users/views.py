from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .decorators import student_required,faculty_required
from urllib.parse import urlencode

#To encode a login redirect message string into query string parameter
loginRedirectMessage = urlencode({'msg' : 'Please Login' })

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
        data = {}
        msg = request.GET.get('msg')
        if msg is not None:
            data["errorMessage"] = msg
        nextUrl = request.GET.get('next')
        if nextUrl is not None:
            data["next"] = nextUrl
        return render(request, "users/login.html",data)
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

@login_required(login_url='/users/login?'+loginRedirectMessage)
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


'''
Function to redirect user to custom 404 Error Page 
'''   


def pageNotFound(request,exception):
    response  = render (request,'404.html')
    response.status_code = 404
    return response


'''
Function to redirect user to custom 404 Error Page 
'''   


def internalServerError(request):
    response  = render (request,'500.html')
    response.status_code = 500
    return response
