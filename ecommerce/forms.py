from django import forms

from core.models import Book, BookPages, Category, BookCategory, ContactReplies, Page, Collection, BookCollection, Tag, Tag

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'name',
            'author',
            'about_author',
            'book_image',
            'author_avatar',
            'desc',
            'subtitle',
            'pdf_link',
            'tags',
            'searchable',
            'show',
            'for_who',
            'is_today',
            'is_paid',
            'is_recent_books',
            'is_active',
        )
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'author':forms.TextInput(attrs={"class":"form-control"}),
            'about_author':forms.Textarea(attrs={"class":"form-control"}),
            'book_image':forms.FileInput(attrs={"class":"form-control"}),
            'author_avatar':forms.FileInput(attrs={"class":"form-control"}),
            'desc':forms.Textarea(attrs={"class":"form-control"}),
            'subtitle':forms.TextInput(attrs={"class":"form-control"}),
            'pdf_link':forms.TextInput(attrs={"class":"form-control"}),
            'tags':forms.SelectMultiple (attrs={"class":"form-control"}),
            'searchable':forms.NumberInput(attrs={"class":"form-control"}),
            'show':forms.NumberInput(attrs={"class":"form-control"}),
            'for_who':forms.TextInput(attrs={"class":"form-control"}),
            'is_today':forms.NullBooleanSelect(attrs={"class":"form-control"}),
            'is_paid':forms.NullBooleanSelect(attrs={"class":"form-control"}),
            'is_recent_books':forms.NullBooleanSelect(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",
            "category_image",
            "desc",
            "searchable",
            "is_active",
        )
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'category_image':forms.FileInput(attrs={"class":"form-control"}),
            'desc':forms.Textarea(attrs={"class":"form-control"}),
            'searchable':forms.NumberInput(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),
        }

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = (
            "category_id",
            "book_id",
            "is_active",
        )
        widgets = {
            'category_id':forms.Select(attrs={"class":"form-control"}),
            'book_id':forms.Select(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),

        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
            "page",
            "is_active",
        )
        widgets = {
            'page':forms.Textarea(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),
        }

class BookPagesForm(forms.ModelForm):
    class Meta:
        model = BookPages
        fields = (
            "page",
            "book_id",
            "is_active",
        )
        widgets = {
            'page':forms.Select(attrs={"class":"form-control"}),
            'book_id':forms.Select(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),

        }


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = (
            "name",
            "collection_image",
            "desc",
            "searchable",
            "show",
            "is_paid",
            "is_active",
        )
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'collection_image':forms.FileInput(attrs={"class":"form-control"}),
            'desc':forms.Textarea(attrs={"class":"form-control"}),
            'searchable':forms.NumberInput(attrs={"class":"form-control"}),
            'show':forms.NumberInput(attrs={"class":"form-control"}),
            'is_paid':forms.NullBooleanSelect(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),

        }

class BookCollectionForm(forms.ModelForm):
    class Meta:
        model = BookCollection
        fields = (
            'book_id',
            'collection_id',
            'is_active',
        )
        widgets = {
            'book_id':forms.Select(attrs={"class":"form-control"}),
            'collection_id':forms.Select(attrs={"class":"form-control"}),
            'is_active':forms.NullBooleanSelect(attrs={"class":"form-control"}),
        }

class ContactReplayForm(forms.ModelForm):
    class Meta:
        model = ContactReplies
        fields = (
            "contact_id",
            "sender_id",
            "receiver_id",
            "replay",
        )
        widgets = {
            'contact_id':forms.Select(attrs={"class":"form-control"}),
            'sender_id':forms.Select(attrs={"class":"form-control"}),
            'receiver_id':forms.Select(attrs={"class":"form-control"}),
            'replay':forms.Textarea(attrs={"class":"form-control"}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            "name",
        )
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
        }