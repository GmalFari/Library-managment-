from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from .models import * 
from .forms import BookForm, CategoryForm
from django.urls import reverse
# Create your views here.

def books(request):
    if request.method == 'POST':
        add_cat = CategoryForm(request.POST)
        if add_cat.is_valid():
            add_cat.save()
            
    search = Books.objects.all()
    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name'] 
        if title:
            search = search.filter(title__icontains=title)
    return render(request, 'pages/books.html', {
        'books' :search,
        'category': Category.objects.all(),
        'formcat':CategoryForm(),
    })


def index(request):
    # add category
    if request.method == 'POST':
        add_cat = CategoryForm(request.POST)
        if add_cat.is_valid():
            add_cat.save()
            
    # add book
    if request.method == 'POST':

        add_book = BookForm(request.POST,request.FILES)
        if add_book.is_valid():
            add_book.save()
    context = {
        'books':Books.objects.all(), # access field
        'category': Category.objects.all(),
        'form':BookForm(),
        'formcat':CategoryForm(),
        'allbooks': Books.objects.filter(active=True).count(),
        'availablebooks':Books.objects.filter(status='available').count(),
        'rentalbooks':Books.objects.filter(status='rental').count(),
        'soldbooks':Books.objects.filter(status='sold').count(),
    }
    print(context['availablebooks'])
    return render(request,'pages/index.html',context)






def update(request,id):
    book_id = Books.objects.get(id=id) # GET object from database
    if request.method == 'POST': # check from request
        book_save = BookForm(request.POST,request.FILES,instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        book_save = BookForm(instance=book_id)
    return render(request, 'pages/update.html',{
        'updateform':book_save,
    } )


def delete(request,id):
    book_id = get_object_or_404(Books,id=id)
    if request.method =='POST':
        book_id.delete()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'pages/delete.html')

