from django.shortcuts import render, redirect
from BRM.forms import NewBookForm,SearchForm
from django.http import HttpResponse, HttpResponseRedirect
from BRM import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages

def home(request):
    res=render(request,'BRM/home.html')
    return res

def userSignup(request):
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']

        if password1==password2 :
            if User.objects.filter(username=username).exists():
                return redirect('/BRM/signup')
            elif User.objects.filter(email=email).exists():
                return redirect('/BRM/signup')
            else:
                user=User.objects.create_user(username=username, password=password1,email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('/BRM/login')
        else:
            return redirect('/BRM/signup')
    return render(request, 'BRM/signup_book.html')


def userLogin(request):
    data={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect('/BRM/view-books')
        else:
            data['error']="Username or password is incorrect"
            res=render(request,'BRM/user_login.html',data)
            return res
    else:
        return render(request,'BRM/user_login.html',data)

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('BRM/login/')

@login_required(login_url="/BRM/login/")
def searchBook(request):
    form=SearchForm()
    res=render(request,'BRM/search_book.html',{'form':form})
    return res

@login_required(login_url="/BRM/login/")
def search(request):
    form=SearchForm(request.POST)
    books=models.Book.objects.filter(title=form.data['title'])
    res=render(request,'BRM/search_book.html',{'form':form,'books':books})
    return res

def deleteBook(request):
    bookid=request.GET['bookid']
    book=models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('/BRM/view-books')

@login_required(login_url="/BRM/login/")
def editBook(request):
    book=models.Book.objects.get(id=request.GET['bookid'])
    fields={'title':book.title,'price':book.price,'author':book.author,'publisher':book.publisher}
    form=NewBookForm(initial=fields)
    res=render(request,'BRM/edit_book.html',{'form':form,'book':book})
    return res

@login_required(login_url="/BRM/login/")
def edit(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.id=request.POST['bookid']
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    return HttpResponseRedirect('/BRM/view-books')

@login_required(login_url="/BRM/login/")
def viewBooks(request):
    books=models.Book.objects.all()
    res=render(request,'BRM/view_book.html',{'books':books})
    return res

@login_required(login_url="/BRM/login/")
def newBook(request):
    form=NewBookForm()
    res=render(request,'BRM/new_book.html',{'form':form})
    return res

@login_required(login_url="/BRM/login/")
def add(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    s="Redord Stored<br><a href='/BRM/view-books'>View all Books</a>"
    return HttpResponse(s)
