from django.shortcuts import render
from rest_framework import serializers
from rest_framework.serializers import Serializer

# Create your views here.
from .models import Book , BookCategory, Category, BookCollection, Collection, Page, Libs
from .serializers import (BookSerializer, BookCategorySerializer, CategoryBookSerializer, CategoryLast10BookSerializer, 
BookCollectionSerializer, FavoriteBookSerializer, BookPagesSerializer, PageSerializer, FavoritePageSerializer, LibsSerializer,
RetrieveLibsSerializer)
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





        