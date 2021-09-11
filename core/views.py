import re
from django.shortcuts import render
from fcm_django.models import FCMDevice

from .models import (Book , BookCategory, Category, BookCollection, Collection, Page, Libs, Contact, NewContact,
ContactReplies)

from .serializers import (BookSerializer, BookCategorySerializer, CategoryBookSerializer, CategoryLast10BookSerializer, 
BookCollectionSerializer, FavoriteBookSerializer, BookPagesSerializer, NewContactSerializer, PageSerializer, FavoritePageSerializer, LibsSerializer,
RetrieveLibsSerializer, CreateContactSerializer, CreateNewContactSerializer, ContactSerializer, CreateContactRepliesSerializer, ContactRepliesSerializer)

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication


class BooksListMethod(viewsets.ViewSet):

    permission_classes = [AllowAny]
    queryset = Book.objects.none()

    def list(self, request):
        user_id = request.user.id
        books = Book.objects.all().filter(is_active=True)
        today_book = request.GET.get("today")
        if (today_book == "True"):
            books = Book.today_books.all()
        recent_books = request.GET.get("recent")
        if (recent_books == "True"):
            books = Book.recent_books.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data, status=200)
    
    def retrieve(self, request, pk):
        user_id = request.user
        books = Book.objects.all().filter(is_active=True)
        book = books.filter(id=pk)
        if len(book) != 0:
            show_book = Book.objects.get(id=pk)
            book.update(show = show_book.show + 1)
            serializer = BookSerializer(book, many=True)
            return Response(serializer.data, status=200)
        return Response("Book not found!", status=404)

class BookCategoryMethod(viewsets.ViewSet):

    permission_classes = [AllowAny]
    queryset = BookCategory.objects.none()

    def list(self, request):
        categorys = Category.objects.all().filter(is_active=True)
        last10_books = request.GET.get("last10")
        all_books = request.GET.get("all")
        if last10_books == "True":
            serializer = CategoryLast10BookSerializer(categorys, many=True)
        if all_books == "True":
            serializer = CategoryBookSerializer(categorys, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk):
        last10_books = request.GET.get("last10")
        all_books = request.GET.get("all")
        categorys = Category.objects.all().filter(is_active=True)
        category = categorys.filter(id=pk)
        if len(category) != 0:
            serializer = CategoryBookSerializer(category, many=True)
            if last10_books == "True":
                serializer = CategoryLast10BookSerializer(category, many=True)
            if all_books == "True":
                serializer = CategoryBookSerializer(category, many=True)
            return Response(serializer.data, status=200)
        return Response("Category not found!", status=404)

    
class BookCollectionMethod(viewsets.ViewSet):

    permission_classes = [AllowAny]
    queryset = BookCollection.objects.none()

    def list(self, request):
        collection = Collection.objects.all().filter(is_active=True)
        serializer = BookCollectionSerializer(collection, many=True)
        return Response(serializer.data, status=200)
    
    def retrieve(self, request, pk):
        collections = Collection.objects.all().filter(is_active=True)
        collection = collections.filter(id=pk)
        if len(collection) !=0:
            show_collection = Collection.objects.get(id=pk)
            collection.update(show = show_collection.show + 1)
            serializer = BookCollectionSerializer(collection, many=True)
            return Response(serializer.data, status=200)
        return Response("Category not found!", status=404)



class BookFavorites(viewsets.ViewSet):

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.none()

    def create(self, request, pk):
        user_id = request.user.id
        try:
            book = Book.objects.get(id=pk)
        except:
            return Response("Book not found!", status=404)
        
        if book.favorites.filter(id=user_id).exists():
            book.favorites.remove(user_id)
            return Response("Book Removed from favorites Successfully", status=201)
        book.favorites.add(user_id)
        return Response("Book added to favorites successfully", status=201)
    
class BookFavoriteList(viewsets.ViewSet):

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.none()

    def list(self, request):
        user_id = request.user.id
        fav_list = Book.objects.filter(favorites=user_id)
        serializer = FavoriteBookSerializer(fav_list, many=True)
        return Response(serializer.data, status=200)

class BookPagesMethod(viewsets.ViewSet):

    permission_classes = [AllowAny]
    queryset = Book.objects.none()

    def retrieve(self, request, pk):
        books = Book.objects.all().filter(is_active=True)
        book = books.filter(id=pk)
        if len(book) == 0:
            return Response("Book not found!", status=404)
        serializer = BookPagesSerializer(book, many=True)
        return Response(serializer.data, status=200)

class PageFavorites(viewsets.ViewSet):

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Page.objects.none()

    def create(self, request, pk):
        user_id = request.user.id
        try:
            page = Page.objects.get(id=pk)
        except:
            return Response("Book not found!", status=404)
        
        if page.favorites.filter(id=user_id).exists():
            page.favorites.remove(user_id)
            return Response("Page Removed from favorites Successfully", status=201)
        page.favorites.add(user_id)
        return Response("Page added to favorites successfully", status=201)


class PageFavoriteList(viewsets.ViewSet):

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.none()

    def list(self, request):
        user_id = request.user.id
        fav_list = Page.objects.filter(favorites=user_id)
        serializer = FavoritePageSerializer(fav_list, many=True)
        return Response(serializer.data, status=200)



class LibsMethod(viewsets.ViewSet):
    """
    create:
    state
    page_id
    book_id
    """

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.none()

    def create(self, request):
        user_id = request.user.id
        data = JSONParser().parse(request)
        page_id = data['page_id']
        book_id = data['book_id']
        if page_id != None:
            try:
                Page.objects.get(id=page_id)
            except:
                return Response("page not found!", status=404)
        if book_id != None:
            try:
                Book.objects.get(id=book_id)
            except:
                return Response("Book not found!", status=404)
        libsdata = {"page_id": page_id, "book_id": book_id, "user_id": user_id}
        lib = Libs.objects.filter(page_id=page_id, book_id=book_id, user_id=user_id)
        if len(lib) != 0:
            lib.delete()
            return Response("object removed successfully!", status=200)
        serializer = LibsSerializer(data=libsdata)
        if serializer.is_valid():
            serializer.save()
            return Response("Object created Successfully!", status=201)
    
    def list(self, request):
        user_id = request.user.id
        libs = Libs.objects.filter(user_id=user_id)
        ser = RetrieveLibsSerializer(libs, many=True)
        return Response(ser.data, status=200)


class ContactsMethod(viewsets.ViewSet):

    authentication_classes=[JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.none()

    def create(self, request):
        user_id = request.user.id
        data = JSONParser().parse(request)
        email = data['email']
        msg = data["msg"]
        contact_data = {"user_id":user_id, "email":email, "msg":msg}
        serializer = CreateContactSerializer(data=contact_data)
        if serializer.is_valid():
            serializer.save()
            return Response("Contact created successfully", status=201)
        return Response("Invalid data!", status=400)
    
    permission_classes = [IsAuthenticated]
    def list(self, request):
        contacts = Contact.objects.all()
        ser = ContactSerializer(contacts, many=True)
        return Response(ser.data, status=200)

    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk):
        contact = Contact.objects.all().filter(id=pk)
        if len(contact) == 0:
            return Response("Contact not found!", status=404)
        ser = ContactSerializer(contact, many=True)
        return Response(ser.data, status=200)


class NewContactMethod(viewsets.ViewSet):

    permission_classes = [AllowAny]
    queryset = NewContact.objects.none()

    def create(self, request):
        device = FCMDevice.objects.all().first().id
        data = JSONParser().parse(request)
        email = data['email']
        msg = data["msg"]
        new_contact_data = {"device":device, "email":email, "msg":msg}
        ser = CreateNewContactSerializer(data=new_contact_data)
        if ser.is_valid():
            ser.save()
            return Response("Contact created successfully", status=201)
        return Response("Invalid data!", status=400)
    
    permission_classes = [IsAuthenticated]
    def list(self, request):
        contacts = NewContact.objects.all()
        ser = NewContactSerializer(contacts, many=True)
        return Response(ser.data, status=200)

    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk):
        contact = NewContact.objects.all().filter(id=pk)
        if len(contact) == 0:
            return Response("Contact not found!", status=404)
        ser = NewContactSerializer(contact, many=True)
        return Response(ser.data, status=200)

class ContactRepliesMethod(viewsets.ViewSet):

    queryset = NewContact.objects.none()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = JSONParser().parse(request)
        sender_id = FCMDevice.objects.all().first().id
        contact_id = data["contact_id"]
        replay = data['replay']
        try:
            receiver = NewContact.objects.get(id=contact_id)
        except:
            return Response("Contact id not found!", status=404)
        receiver_id = receiver.device.id
        ser_data = {"contact_id":contact_id, "sender_id":sender_id, "receiver_id":receiver_id, "replay":replay}
        ser = CreateContactRepliesSerializer(data=ser_data)
        if ser.is_valid():
            ser.save()
            return Response("Contact replay created successfully!", status=201)
        return Response("Invalid data!", status=400)
    
    def list(self, request):
        contact_replies = ContactReplies.objects.all()
        ser = ContactRepliesSerializer(contact_replies, many=True)
        return Response(ser.data, status=200)
    
    def retrieve(self, request, pk):
        contact_replay = ContactReplies.objects.all().filter(id=pk)
        if len(contact_replay) == 0:
            return Response("Contact_replay not found!", status=404)
        ser = ContactRepliesSerializer(contact_replay, many=True)
        return Response(ser.data, status=200)



        

