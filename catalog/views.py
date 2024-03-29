from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import *
from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .forms import CommentForm,BookOrderForm
from django.contrib.auth.decorators import login_required

def index(request):
    books = Book.objects.all().count()
    authors = Author.objects.all().count()
    messages.success(request,'Welcome')
    return render(request,'catalog/index.html',context={'books':books,'authors':authors})



def books_list(request): 
    genres = Genre.objects.all()
    books = Book.objects.all()
    paginator = Paginator(books,3)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, "catalog/books.html", {'genres': genres, 'books': books}) 


def book_detail(request, book_slug):
    book = get_object_or_404(Book, book_slug=book_slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.book = book
        new_comment.author = request.user
        new_comment.save()
    else:
        form = CommentForm()
    comments = Comments.objects.filter(book=book).order_by('-created') 
    return render(request,'catalog/book_detail.html', {'book': book,'comments':comments,'form':form})

def book_author(request,slug):
    author = get_object_or_404(Author,slug=slug)
    books = Book.objects.filter(author=author)
    return render(request,'catalog/author.html',{'author':author,'books':books})

def book_genre(request,id):
    genre = Genre.objects.get(pk = id)
    genres = Genre.objects.all()
    books = Book.objects.filter(genre_id = id)
    if len(books) < 1:
        messages.error(request,'Sorry we have no books in this category right now')
        return redirect('books')
        
    else:
        return render(request,'catalog/book_genre.html',{"genre":genre,'books':books,'genres':genres})

def authors(request):
    authors = Author.objects.all()
    return render(request,'catalog/authors.html',{"authors":authors})


def search(request):
    query = request.GET.get('query')
    books = Book.objects.filter(
        Q(title__icontains = query) |
        Q(description__icontains = query)
    )
    if books:
        return render(request,'catalog/search.html',{"books":books})
    else:
        return redirect('books')

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Succesfully registered')
            return redirect('books')

    return render(request, "account/sign_up.html", {'form': form,})

def log_out(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('books')

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Successfully logged in',fail_silently=False)
                return redirect('books')
            else:
                messages.debug(request,"Username or password is incorrect")
        else:
            messages.error(request,'Incorect information')
    return render(request,'account/sign_in.html',{"form":form})

def edit_book(request,book_slug):
    book = Book.objects.get(book_slug=book_slug)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.save()
        return redirect('/')
    return render(request,'catalog/edit.html',{'book':book})

def delete_book(request,book_slug):
    book = get_object_or_404(Book,book_slug = book_slug)
    book.delete()
    return redirect('/')

@login_required(login_url='sign_in')
def order_book(request):
    form = BookOrderForm()
    if request.method == "POST":
        form = BookOrderForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data.get('book')
            imprint = form.cleaned_data.get('imprint')
            user = request.user
            book_instance = BookInstance(book=book, imprint=imprint,user=user)
            book_instance.save()
            messages.info(request, "Order has been accepted")
            return redirect('books')
    return render(request, "catalog/order_book.html", {'form': form})

@login_required(login_url='sign_in')
def user_order(request):
    orders = BookInstance.objects.filter(user=request.user)
    if len(orders) < 1:
        messages.info(request,"You haven't ordered any book\nLet's order it")
        return redirect('order')
    else:
        return render(request, "catalog/user_orders.html", {'orders': orders})