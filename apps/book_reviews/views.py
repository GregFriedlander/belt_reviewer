from __future__ import unicode_literals 
import bcrypt
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages 


# Create your views here.

def index(request):
    
    return render(request, "book_reviews/login.html")

def register(request):
    if request.method == "POST":
        errors = Users.objects.validate_reg(request.POST)
        if len(errors):
            for key in errors:
                messages.error(request, errors[key])
            return redirect('/')
    
    pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw)
    request.session['id'] = user.id
    request.session['name'] = user.name
    request.session['alias'] = user.alias
    request.session['email'] = user.email
        
    
    return redirect('/books')

def login(request):
    login_return = Users.objects.validate_login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name'] = login_return['user'].name
        request.session['alias'] = login_return['user'].alias
        request.session['email'] = login_return['user'].email
        return redirect('/books')
    else:
        messages.error(request, login_return['error'])
        return redirect('/')

def books(request):
    books = Books.objects.all()
    reviews = Reviews.objects.order_by('-created_at')[:3]
    context = {
        "books": books,
        "reviews": reviews
    }
    return render(request, "book_reviews/homepage.html", context)

def add(request):
    available_authors = Authors.objects.all()
    context = {
        "authors": available_authors
    }
    return render(request, "book_reviews/addbook.html", context)

def processreview(request):
    if len(request.POST['author_name']) > 0:
        author = Authors.objects.create(name=request.POST['author_name'])
    else:
        author = Authors.objects.get(name=request.POST['author_list'])
    book = Books.objects.create(title=request.POST['book_title'], author=author)
    book_id= book.id
    user = Users.objects.get(id=request.session['id'])
    Reviews.objects.create(desc=request.POST['review'], rating=request.POST['rating'], user=user, book=book)
    return redirect('/books/{}'.format(book_id))

def addreview(request, book_id):
    user = Users.objects.get(id = request.session['id'])
    book = Books.objects.get(id = book_id)
    Reviews.objects.create(desc=request.POST['add_review'], rating=request.POST['rating'], user=user, book=book)
    return redirect('/books/{}'.format(book_id))


def bookview(request, book_id):
    books = Books.objects.get(id=book_id)
    reviews = Books.objects.get(id=book_id).reviews.all()
    context = {
        "books": books,
        "reviews": reviews
    }
    return render(request, "book_reviews/bookreview.html", context)

def userdisplay(request, user_id):
    user = Users.objects.get(id=user_id)
    reviews = Reviews.objects.filter(user = user)
    review_count = len(reviews)
    context = {
        "user": user,
        "review_count": review_count,
        "reviews": reviews
    }
    return render(request, "book_reviews/userreviews.html", context)


def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


def delete(request, book_id):
    r = Reviews.objects.get(id=request.POST['review_id'])
    r.delete()
    return redirect('/books/{}'.format(book_id))
