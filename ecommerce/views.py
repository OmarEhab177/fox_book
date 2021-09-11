from django.http import request, HttpResponseRedirect, response
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import BookForm, CategoryForm, BookCategoryForm, ContactReplayForm, PageForm, BookPagesForm, CollectionForm, BookCollectionForm, TagForm

from core.models import Book, Category, BookCategory, ContactReplies, Page, BookPages, Collection, BookCollection, NewContact, Tag


# Products
class ProductsView(LoginRequiredMixin,View):
    def get(self, request):
        all_books = Book.objects.all()
        today_books = Book.today_books.all()
        recent_books = Book.recent_books.all()
        greeting = {}
        greeting['title'] = "Products"
        greeting['pageview'] = "Ecommerce"
        greeting['all_books'] = all_books
        greeting['today_books'] = today_books
        greeting['recent_books'] = recent_books

        return render(request, 'menu/ecommerce/ecommerce-products.html',greeting)



# Product Details
class ProductDetailsView(LoginRequiredMixin,View):
    def get(self, request):
        # books = Book.objects.all()
        # book = books.filter(id=pk)
        greeting = {}
        greeting['title'] = "Product Detail"
        greeting['pageview'] = "Ecommerce"
        # greeting['book'] = book
        return render(request, 'menu/ecommerce/ecommerce-product-detail.html',greeting)


class BookDetailsView(LoginRequiredMixin,View):
    def get(self, request, pk):
        books = Book.objects.all()
        book = get_object_or_404(books, id=pk)
        # try:
        book_pages = BookPages.objects.filter(book_id=pk).order_by("id")
        # except:
            # book_pages = BookPages.objects.get(book_id=pk) 
        # print("book_page: ", book_pages)
        context = {
            'title': "Book Detail",
            "pageview": "Ecommerce",
            "book": book,
            "book_pages":book_pages
        }
        return render(request, "menu/ecommerce/book-detail.html", context)


class AddBookView(LoginRequiredMixin,View):
    form_class = BookForm
    initial = {'key': 'value'}
    template_name =  "menu/ecommerce/add-book.html"
    def get(self, request, *args, **kwargs):
        add_book = self.form_class(initial=self.initial)
        context = {
            "form":add_book,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # if request.method == "POST":
        add_book = BookForm(request.POST, request.FILES)
        if add_book.is_valid():
            add_book.save()
            return HttpResponseRedirect('/ecommerce/products')

        context = {
            "form": add_book,
        }
        
        return render(request, self.template_name, context)



@login_required
def update_book(request, pk):
    books = Book.objects.all()
    book = get_object_or_404(books, id=pk)
    if request.method == "POST":
        edit_book = BookForm(request.POST, request.FILES, instance=book)
        if edit_book.is_valid():
            edit_book.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj =  BookForm(instance=book)

    context = {
        "form": obj,
    }
    template =  "menu/ecommerce/edit-book.html"
    return render(request, template, context)


@login_required
def delete_book(request, pk):
    books = Book.objects.all()
    book = get_object_or_404(books, id=pk)
    if request.method == "POST":
        book.delete()
        return redirect('/ecommerce/products')
    template = "menu/ecommerce/delete-book.html"
    return render(request, template)


class CategoriesViews(LoginRequiredMixin,View):

    def get(self, request):
        categories = Category.objects.all()
        
        greeting = {}
        greeting['title'] = "Categories"
        greeting['pageview'] = "Ecommerce"
        greeting['categories'] = categories
       

        return render(request, 'menu/ecommerce/book-categories-list.html',greeting)
    
class CategoryDetail(LoginRequiredMixin,View):

    def get(self, request, pk):
        categories = Category.objects.all()
        category = get_object_or_404(categories, id=pk)
        cat_books = BookCategory.objects.filter(category_id=category).order_by("id")
        # print("book_cat: ", cat_books.book_id)

        greeting = {}
        greeting['title'] = "Category"
        greeting['pageview'] = "Ecommerce"
        greeting['category'] = category
        greeting['cat_books'] = cat_books


        return render(request, 'menu/ecommerce/book-category-detail.html',greeting)


@login_required
def add_category(request):
    categoryForm = CategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if categoryForm.is_valid():
            categoryForm.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        categoryForm = CategoryForm()
    
    context = {
        "form":categoryForm,
    }
    template = 'menu/ecommerce/add-category.html'
    return render(request, template, context)


@login_required
def update_category(request, pk):
    categories = Category.objects.all()
    category = get_object_or_404(categories, id=pk)
    if request.method == "POST":
        edit_book = CategoryForm(request.POST, request.FILES, instance=category)
        if edit_book.is_valid():
            edit_book.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj =  CategoryForm(instance=category)

    context = {
        "form": obj,
    }
    template =  "menu/ecommerce/edit-category.html"
    return render(request, template, context)


@login_required
def delete_category(request, pk):
    categories = Category.objects.all()
    category = get_object_or_404(categories, id=pk)
    if request.method == "POST":
        category.delete()
        return redirect('/ecommerce/products')
    template = "menu/ecommerce/delete-category.html"
    return render(request, template)


class BookCategoriesView(LoginRequiredMixin,View):

    def get(self, request):
        book_categories = BookCategory.objects.all()
        
        greeting = {}
        greeting['title'] = "Categories"
        greeting['pageview'] = "Ecommerce"
        greeting['book_categories'] = book_categories
       
        return render(request, 'menu/ecommerce/book_categories-list.html',greeting)

class BookCategoryDetail(LoginRequiredMixin,View):

    def get(self, request, pk):
        book_categories = BookCategory.objects.all()
        book_category = get_object_or_404(book_categories, id=pk)

        greeting = {}
        greeting['title'] = "Category"
        greeting['pageview'] = "Ecommerce"
        greeting['book_category'] = book_category

        return render(request, 'menu/ecommerce/book-category-detail.html',greeting)


@login_required
def add_book_category(request):
    book_categoryForm = BookCategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if book_categoryForm.is_valid():
            book_categoryForm.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        book_categoryForm = BookCategoryForm()
    
    context = {
        "form":book_categoryForm,
    }
    template = 'menu/ecommerce/add-book-category.html'
    return render(request, template, context)


@login_required
def add_bookToCategory(request, pk):
    initial = {"category_id": pk}
    book_categoryForm = BookCategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if book_categoryForm.is_valid():
            book_categoryForm.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        book_categoryForm = BookCategoryForm(initial=initial)
    
    context = {
        "form":book_categoryForm,
    }
    template = 'menu/ecommerce/add-bookToCategory.html'
    return render(request, template, context)


@login_required
def update_book_category(request, pk):
    book_categories = BookCategory.objects.all()
    book_category = get_object_or_404(book_categories, id=pk)
    if request.method == "POST":
        edit_book = BookCategoryForm(request.POST, request.FILES, instance=book_category)
        if edit_book.is_valid():
            edit_book.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj =  BookCategoryForm(instance=book_category)

    context = {
        "form": obj,
    }
    template =  "menu/ecommerce/edit-book-category.html"
    return render(request, template, context)


@login_required
def delete_book_category(request, pk):
    book_categories = BookCategory.objects.all()
    book_category = get_object_or_404(book_categories, id=pk)
    if request.method == "POST":
        book_category.delete()
        return redirect('/ecommerce/products')
    template = "menu/ecommerce/delete-book-category.html"
    return render(request, template)


@login_required
def add_page(request):
    page_form = PageForm(request.POST)
    if request.method == "POST":
        if page_form.is_valid():
            page_form.save()
            return HttpResponseRedirect("products")
    else:
        obj = PageForm()

    context = {
        "form": obj
    }
    template = 'menu/ecommerce/add-page.html'
    return render(request, template, context)

@login_required
def add_pageTOBook(request, pk):
    page_form = PageForm(request.POST)
    if request.method == "POST":
        if page_form.is_valid():
            page_form.save()
            page = Page.objects.all().order_by("-id")[0]
            # print("page: ", page)
            book = Book.objects.get(id=pk)
            book_page = BookPages(page=page, book_id=book)
            book_page.save()
            
            return HttpResponseRedirect("/ecommerce/products")
    else:
        obj = PageForm()

    context = {
        "form": obj
    }
    template = 'menu/ecommerce/add-pageToBook.html'
    return render(request, template, context)

@login_required
def retrieve_page(request, pk):
    pages = Page.objects.all()
    page = get_object_or_404(pages, id=pk)

    context = {
        'page':page
    }
    template = 'menu/ecommerce/page_detail.html'
    return render(request, template, context)

@login_required
def update_page(request, pk):
    pages = Page.objects.all()
    page = get_object_or_404(pages, id=pk)
    if request.method == "POST":
        edit_page = PageForm(request.POST, instance=page)
        if edit_page.is_valid():
            edit_page.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj =  PageForm(instance=page)

    context = {
        "form": obj,
    }
    template =  "menu/ecommerce/edit-page.html"
    return render(request, template, context)



@login_required
def delete_page(request, pk):
    pages = Page.objects.all()
    page = get_object_or_404(pages, id=pk)
    if request.method == "POST":
        page.delete()
        return HttpResponseRedirect('/ecommerce/products')
    template = "menu/ecommerce/delete-page.html"
    return render(request, template)


@login_required
def add_book_page(request):
    book_page_form = BookPagesForm(request.POST)
    if request.method == "POST":
        if book_page_form.is_valid():
            book_page_form.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj = BookPagesForm()
    
    context = {
        "form": obj
    }

    template = 'menu/ecommerce/add-book-page.html'
    return render(request, template, context)


@login_required
def add__page_to_book(request, pk):
    initial = {'book_id': pk}
    book_page_form = BookPagesForm(request.POST, initial=initial)
    if request.method == "POST":
        if book_page_form.is_valid():
            book_page_form.save()
            return HttpResponseRedirect('/ecommerce/products')
    else:
        obj = BookPagesForm(initial=initial)
    
    context = {
        "form": obj
    }

    template = 'menu/ecommerce/add-page-to-book.html'
    return render(request, template, context)



@login_required
def collection_list(request):
    collections = Collection.objects.all()
    context = {
        'collections': collections
    }
    template = 'menu/ecommerce/book-collections-list.html'
    return render(request, template, context)


@login_required
def collection_detail(request, pk):
    collections = Collection.objects.all()
    coll = get_object_or_404(collections, id=pk)
    book_colls = BookCollection.objects.filter(collection_id=coll).order_by("id")
    context = {
        'coll': coll,
        "book_colls": book_colls
    }
    template = 'menu/ecommerce/book-collection-detail.html'
    return render(request, template, context)



@login_required
def add_bookToCollection(request, pk):
    initial = {"collection_id": pk}
    book_collectionForm = BookCollectionForm(request.POST, request.FILES)
    if request.method == "POST":
        if book_collectionForm.is_valid():
            book_collectionForm.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        book_collectionForm = BookCollectionForm(initial=initial)
    
    context = {
        "form":book_collectionForm,
    }
    template = 'menu/ecommerce/add-bookToCollection.html'
    return render(request, template, context)



@login_required
def add_collection(request):
    collection_form = CollectionForm(request.POST, request.FILES)
    if request.method == "POST":
        if collection_form.is_valid():
            collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = CollectionForm()
    
    context = {
        "form": obj
    }
    template = "menu/ecommerce/add-collection.html"
    return render(request, template, context)


@login_required
def update_collection(request, pk):
    collections = Collection.objects.all()
    collection = get_object_or_404(collections, id=pk)
    if request.method == "POST":
        collection_form = CollectionForm(request.POST, request.FILES, instance=collection)
        if collection_form.is_valid():
            collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = CollectionForm(instance=collection)
    context = {
        "form":obj
    }
    template = "menu/ecommerce/edit_collection.html"
    return render(request, template, context)


@login_required
def delete_collection(request, pk):
    collections = Collection.objects.all()
    collection = get_object_or_404(collections, id=pk)
    if request.method == "POST":
        collection.delete()
        return redirect('/ecommerce/collections')
    template = "menu/ecommerce/delete-collection.html"
    return render(request, template)



@login_required
def add_book_collection(request):
    book_collection_form = BookCollectionForm(request.POST)
    if request.method == "POST":
        if book_collection_form.is_valid():
            book_collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = BookCollectionForm()
    
    context = {
        "form": obj
    }
    template = "menu/ecommerce/add-book-collection.html"
    return render(request, template, context)



@login_required
def add_book_to_collection(request, pk):
    initial = {'collection_id': pk}
    book_collection_form = BookCollectionForm(request.POST, initial=initial)
    if request.method == "POST":
        if book_collection_form.is_valid():
            book_collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = BookCollectionForm(initial=initial)
    
    context = {
        "form": obj
    }
    template = "menu/ecommerce/add-book-to-collection.html"
    return render(request, template, context)

@login_required
def add_collection_to_book(request, pk):
    initial = {'book_id': pk}
    book_collection_form = BookCollectionForm(request.POST, initial=initial)
    if request.method == "POST":
        if book_collection_form.is_valid():
            book_collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = BookCollectionForm(initial=initial)
    
    context = {
        "form": obj
    }
    template = "menu/ecommerce/add-collection-to-book.html"
    return render(request, template, context)


@login_required
def update_book_collection(request, pk):
    book_collections = BookCollection.objects.all()
    book_collection = get_object_or_404(book_collections, id=pk)
    if request.method == "POST":
        book_collection_form = BookCollectionForm(request.POST, instance=book_collection)
        if book_collection_form.is_valid():
            book_collection_form.save()
            return HttpResponseRedirect('/ecommerce/collections')
    else:
        obj = BookCollectionForm(instance=book_collection)
    context = {
        "form": obj
    }
    template = "menu/ecommerce/edit-book-collection.html"
    return render(request, template, context)



@login_required
def book_collection_list(request):
    book_collections = BookCollection.objects.all()
    context = {
        "book_collections":book_collections
    }
    template = "menu/ecommerce/book-collections-list.html"
    return render(request, template, context)



@login_required
def delete_book_collection(request, pk):
    book_collections = BookCollection.objects.all()
    book_collection = get_object_or_404(book_collections, id=pk)
    if request.method == "POST":
        book_collection.delete()
        return redirect('/ecommerce/collections')
    template = "menu/ecommerce/delete-book-collection.html"
    return render(request, template)



@login_required
def contacts_list(request):
    contacts = NewContact.objects.all()
    context = {
        'contacts': contacts
    }
    template = 'menu/ecommerce/conatcts-list.html'
    return render(request, template, context)


@login_required
def contact_detail(request, pk):
    contacts = NewContact.objects.all()
    contact = get_object_or_404(contacts, id=pk)
    contact_reps = ContactReplies.objects.filter(contact_id=pk).order_by("-id")
    context = {
        'contact': contact,
        "contact_reps": contact_reps
    }
    template = 'menu/ecommerce/conatct-detail.html'
    return render(request, template, context)


@login_required
def delete_contact(request, pk):
    contacts = NewContact.objects.all()
    contact = get_object_or_404(contacts, id=pk)
    if request.method == "POST":
        contact.delete()
        return redirect('/ecommerce/conatcts-list')
    template = "menu/ecommerce/delete-contact.html"
    return render(request, template)



@login_required
def contact_replies_list(request):
    contact_replies = ContactReplies.objects.all()
    context = {
        'contact_replies': contact_replies
    }
    template = 'menu/ecommerce/contact-replies-list.html'
    return render(request, template, context)

@login_required
def contact_replay_detail(request, pk):
    contact_replies = ContactReplies.objects.all()
    contact_replay = get_object_or_404(contact_replies, id=pk)
    context = {
        'contact_replay': contact_replay
    }
    template = 'menu/ecommerce/contact-replay-detail.html'
    return render(request, template, context)


@login_required
def add_contact_replay(request,pk):
    sender_id = request.user
    contacts = NewContact.objects.all()
    contact = get_object_or_404(contacts, id=pk)
    receiver_id = contact.device
    print("contact: ",contact)
    print("sender_id",sender_id)
    print("receiver_id", receiver_id)

    initial = {
        "contact_id":pk, 
        "sender_id":sender_id,
        "receiver_id":receiver_id
    }

    contact_replay_form = ContactReplayForm(request.POST, initial=initial)
    if request.method == "POST":
        if contact_replay_form.is_valid():
            contact_replay_form.save()
            return HttpResponseRedirect('/ecommerce/conatcts-list')
    else:
        obj = ContactReplayForm(initial=initial)
    
    context = {
        "form": obj
    }
    template = "menu/ecommerce/add-contact-replay.html"
    return render(request, template, context)


@login_required
def delete_contact_replay(request, pk):
    contact_replies = ContactReplies.objects.all()
    contact_replay = get_object_or_404(contact_replies, id=pk)
    if request.method == "POST":
        contact_replay.delete()
        return HttpResponseRedirect('/ecommerce/conatcts-list')
    template = "menu/ecommerce/delete-contact-replay.html"
    return render(request, template)


@login_required
def add_tag(request):
    tag_form = TagForm(request.POST)
    if request.method =="POST":
        if tag_form.is_valid():
            tag_form.save()
            return HttpResponseRedirect('/ecommerce/tags')
    else:
        obj = TagForm()
    context = {
        "form": obj
    }
    template = 'menu/ecommerce/add-tag.html'
    return render(request, template, context)

@login_required
def update_tag(request, pk):
    tags = Tag.objects.all()
    tag = get_object_or_404(tags, id=pk)
    tag_form = TagForm(request.POST, instance=tag)
    if request.method =="POST":
        if tag_form.is_valid():
            tag_form.save()
            return HttpResponseRedirect('/ecommerce/tags')
    else:
        obj = TagForm(instance=tag)
    context = {
        "form": obj
    }
    template = 'menu/ecommerce/update-tag.html'
    return render(request, template, context)


@login_required
def tag_list(request):
    tags = Tag.objects.all()
    context = {
        "tags": tags
    }
    template = "menu/ecommerce/tag-list.html"
    return render(request, template, context)


@login_required
def tag_detail(request, pk):
    tags = Tag.objects.all()
    tag = get_object_or_404(tags, id=pk)
    context = {
        "tag": tag
    }
    template = "menu/ecommerce/tag-detail.html"
    return render(request, template, context)

@login_required
def delete_tag(request, pk):
    tags = Tag.objects.all()
    tag = get_object_or_404(tags, id=pk)
    if request.method == "POST":
        tag.delete()
        return HttpResponseRedirect('/ecommerce/tags')

    template = "menu/ecommerce/delete-tag.html"
    return render(request, template)



    





















# Orders
class OrdersView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Orders"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-orders.html',greeting)

# Customers
class CustomersView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Customers"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-customers.html',greeting)

# Cart
class CartView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Cart"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-cart.html',greeting)

# Check-out
class CheckoutView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Checkout"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-checkout.html',greeting)

# Shops
class ShopsView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Shops"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-shops.html',greeting)

# Add Product
class AddProductView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Add Product"
        greeting['pageview'] = "Ecommerce"        
        return render(request, 'menu/ecommerce/ecommerce-add-product.html',greeting)
