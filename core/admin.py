from django.contrib import admin
from .models import (Category, Tag, Book, BookPages, Collection,
UserSearches, BookCollection, Libs, Rates, Plan, UserPlan,
Contacts, ContactReplies, BookCategory,Page)
# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(BookPages)
admin.site.register(Collection)
admin.site.register(UserSearches)
admin.site.register(BookCollection)
admin.site.register(Libs)
admin.site.register(Rates)
admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(Contacts)
admin.site.register(ContactReplies)
admin.site.register(BookCategory)
admin.site.register(Page)