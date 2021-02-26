from django.shortcuts import render, redirect
from .models import Blog, BlogComments
from users.decorators import faculty_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

'''
    Function to get all blog list details
'''


@login_required(login_url='/users/login')
def list(request):
    blogs = Blog.objects.all()
    return render(request, './blog/list.html', {'blogs': blogs})


'''
    Function to create Blog
'''


@login_required(login_url='/users/login')
def create(request):
    if request.method == "GET":
        return render(request, "blog/create.html")

    user = request.user
    title = request.POST['title']
    description = request.POST['description']
    newBlog = Blog(user=user, title=title, description=description)
    newBlog.save()
    return redirect('/blogs/')


'''
    Function to get blog details
'''


@login_required(login_url='/users/login')
def view(request):
    user = request.user

    # if requested classroom not exists then

    try:
        blogId = request.GET['id']
        blog = Blog.objects.get(blogId=blogId)
        # fetch all the class comments belonging to particular blog
        comments = BlogComments.objects.filter(blog=blog)
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    return render(request, './blog/view.html', {'blog': blog, 'comments': comments})


'''
    Function to edit the blog details
'''


@login_required(login_url='/users/login')
def edit(request):
    if request.method == "GET":
        try:
            blogId = request.GET['id']
            blog = Blog.objects.get(blogId = blogId)
            if blog.user != request.user:
                return render(request, 'accessDenied.html', {})
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return render(request, '404.html', {})

        return render(request, "blog/edit.html", {'blog': blog})

    try:
        blogId = request.POST['blogId']
        blog = Blog.objects.get(blogId=blogId)
        if blog.user != request.user:
            return render(request, 'accessDenied.html', {})
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    blog.title = request.POST['title']
    blog.description = request.POST['description']
    blog.save()
    return redirect('/blogs/')


'''
    Function to delete particular blog
'''


@login_required(login_url='/users/login')
def delete(request):
    if request.method == "GET":
        try:
            blogId = request.GET['id']
            blog = Blog.objects.get(blogId=blogId)
            if blog.user != request.user:
                return render(request, 'accessDenied.html', {})
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return render(request, '404.html', {})

        return render(request, "blog/delete.html", {'blog': blog})

    try:
        blogId = request.POST['blogId']
        blog = Blog.objects.get(blogId=blogId)
        if blog.user != request.user:
            return render(request, 'accessDenied.html', {})
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    blog.delete()
    return redirect('/blogs/')


'''
    function to create the blog comments
'''


@login_required(login_url='/users/login')
def commentCreate(request):
    # if requested classroom not exists then
    try:
        blogId = request.POST['blogId']
        blog = Blog.objects.get(blogId=blogId)
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    comment = request.POST["comment"]
    user = request.user
    inputFile = request.FILES.get('inputFile')
    print(comment)
    print(blogId)
    newComment = BlogComments(comment=comment, user=user, blog=blog, attachmentPath=inputFile)
    newComment.save()

    return redirect('/blogs/view/?id' + "=" + blogId)
