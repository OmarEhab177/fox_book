import json
from rest_framework import serializers
from core.models import (Book, BookCategory, Category, Collection,
BookCollection, Page, BookPages, Libs, Contact, NewContact, ContactReplies)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "about_author",
            "book_image",
            "author_avatar",
            "desc",
            "subtitle",
            "pdf_link",
            "tag",
            "searchable",
            "show",
            "for_who",
            "is_today",
            "is_paid",
            "is_recent_books",
            "created_at",
            "updated_at",
            "is_active",
            "favorites",
            "get_rating",
            # "is_favorite"
            
        )

class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "about_author",
            "book_image",
            "author_avatar",
            "desc",
            "subtitle",
            "pdf_link",
            "tag",
            "searchable",
            "show",
            "for_who",
            "is_today",
            "is_paid",
            "is_recent_books",
            "created_at",
            "updated_at",
            "is_active", 
        )
        

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = (
            "id",
            "category_id",
            "book_id",
            "created_at",
            "updated_at",
            "is_active",
        )

class BooksCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = (
            # "id",
            "book_id",
        )
        depth = 1


class Last10Books(serializers.RelatedField):
    def to_representation(self, many=True):
        books = Book.last10_books.all()
        serializer = BookSerializer(books, many=True)
        return {"last10books":serializer.data}


class CategoryLast10BookSerializer(serializers.ModelSerializer):
    books = Last10Books(source="bookcategory_set",  read_only=True)    ## last 10 book in category

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "category_image",
            "desc",
            "searchable",
            "created_at",
            "updated_at",
            "is_active",
            "books",
        )

class CategoryBookSerializer(serializers.ModelSerializer):
    books = BooksCatSerializer(source="bookcategory_set", many=True)  ## return all books in category

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "category_image",
            "desc",
            "searchable",
            "created_at",
            "updated_at",
            "is_active",
            "books",
        )


class RetriveBookCollSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCollection
        fields = (
            # "id",
            "book_id",
        )
        depth = 1


class BookCollectionSerializer(serializers.ModelSerializer):
    books = RetriveBookCollSerializer(source="bookcollection_set", many=True)  ## return all books in collection

    class Meta:
        model = Collection
        fields = (
            "id",
            "name",
            "collection_image",
            "desc",
            "searchable",
            "show",
            "is_paid",
            "created_at",
            "updated_at",
            "is_active",
            "books"
        )

class PageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page
        fields = (
            "id",
            "page",
            "created_at",
            "updated_at",
            "is_active",
            "favorites"
        )

class FavoritePageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page
        fields = (
            "id",
            "page",
            "created_at",
            "updated_at",
            "is_active",
        )

class PageBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookPages
        fields = (
            # "id",
            "page",
        )
        depth = 1

class BookPagesSerializer(serializers.ModelSerializer):
    pages = PageBookSerializer(source="bookpages_set", many=True)
    
    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "about_author",
            "book_image",
            "author_avatar",
            "desc",
            "subtitle",
            "pdf_link",
            "tag",
            "searchable",
            "show",
            "for_who",
            "is_today",
            "is_paid",
            "is_recent_books",
            "created_at",
            "updated_at",
            "is_active",
            "favorites",
            "pages",
        )


class LibsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libs
        fields = (
            "id",
            "page_id",
            "book_id",
            "user_id",
        )

class RetrieveLibsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libs
        fields = (
            "id",
            "page_id",
            "book_id",
        )
        depth = 1

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            "id",
            "user_id",
            "email",
            "msg",
            "read_at",
            "created_at",
            "updated_at"
        )




class CreateContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            "user_id",
            "email",
            "msg",
        )


class NewContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewContact
        fields = (
            "id",
            "device",
            "email",
            "msg",
            "read_at",
            "created_at",
            "updated_at"
        )


class CreateNewContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewContact
        fields = (
            "device",
            "email",
            "msg",
        )


class CreateContactRepliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactReplies
        fields = (
            "contact_id",
            "sender_id",
            "receiver_id",
            "replay",
        )
class ContactRepliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactReplies
        fields = (
            "id",
            "contact_id",
            "sender_id",
            "receiver_id",
            "replay",
            "created_at",
            "updated_at"
        )

