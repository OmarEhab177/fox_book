from enum import unique
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from fcm_django.models import FCMDevice

from .managers import TodayBooks, RecentBook, Last10Books


class Category(models.Model):
    name = models.CharField(max_length=250)
    category_image = models.ImageField(upload_to = 'photos/Categories/%y/%m/%d')
    desc = models.TextField()
    searchable = models.IntegerField()   ##########
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    about_author = models.TextField()
    book_image = models.ImageField(upload_to = 'photos/books/%y/%m/%d')
    author_avatar = models.ImageField(upload_to = 'photos/authors/%y/%m/%d')
    desc = models.TextField(null=True, blank=True)
    subtitle = models.CharField(max_length=250)
    pdf_link = models.CharField(max_length=250)
    tags = models.ManyToManyField(Tag, related_name="book_tags", default=None, blank=True)
    searchable = models.IntegerField(null=True, blank=True)
    show = models.IntegerField(null=True, blank=True)
    for_who = models.CharField(max_length=250)
    is_today = models.BooleanField(default=True)
    is_paid =  models.BooleanField(default=False)
    is_recent_books = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    favorites = models.ManyToManyField(CustomUser, related_name="favorite_books", default=None, blank=True)

    objects = models.Manager()
    today_books = TodayBooks()
    recent_books = RecentBook()
    last10_books = Last10Books()

    class Meta:
        ordering = ('-created_at',)

    def get_rating(self):
        total = sum(int(review['rate']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0

    # def is_favorite(self,request):
    #     fav = self.objects.filter(favorites=request.user.id)
    #     if fav:
    #         return True
    #     return False

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    category_id =  models.ForeignKey(Category, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        unique_together = [
            ('category_id', 'book_id')
        ]
        ordering = ('-created_at',)
    def __str__(self):
        return self.book_id.name + "  in " + self.category_id.name

class Page(models.Model):
    page = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    favorites = models.ManyToManyField(CustomUser, related_name="favorite_pages", default=None, blank=True)

    def __str__(self):
        return self.page[:25]

class BookPages(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE,)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        unique_together = [
            ('page', 'book_id')
        ]


class Collection(models.Model):
    name = models.CharField(max_length=250)
    collection_image = models.ImageField(upload_to = 'photos/collection/%y/%m/%d')
    desc = models.TextField()
    searchable = models.IntegerField()
    show = models.IntegerField()
    is_paid =  models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

class UserSearches(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_searches")
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_book_searches")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="user_category_searches")
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="user_collection_searches")
    category_count = models.IntegerField()
    book_count = models.IntegerField()
    collection_count = models.IntegerField()
    ip_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BookCollection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        unique_together = [
            ('collection_id', 'book_id')
        ]
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.book_id.name + "  in " + self.collection_id.name



class Libs(models.Model):
    page_id = models.ForeignKey(Page, on_delete=models.CASCADE, default=None, blank=True, null=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, default=None, blank=True, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ("book_id", "user_id"),
            ("page_id", "user_id")

        ]


class Rates(models.Model):
    rate = models.PositiveIntegerField(default=1)
    book_id = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        unique_together = [
            ('user_id', 'book_id')
        ]

class Plan(models.Model):
    name = models.CharField(max_length=250)
    desc = models.TextField()
    plan_image = models.ImageField(upload_to = 'photos/plans/%y/%m/%d')
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00 , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserPlan(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    transaction_id = models.IntegerField() ###########
    transaction_data = models.TextField()
    plan_subscribed_at = models.DateTimeField(null=True)
    expired_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
    msg = models.TextField()
    read_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class NewContact(models.Model):
    device = models.ForeignKey(FCMDevice, on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
    msg = models.TextField()
    read_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class ContactReplies(models.Model):
    contact_id = models.ForeignKey(NewContact, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(FCMDevice, on_delete=models.CASCADE, related_name="sender_device")
    receiver_id = models.ForeignKey(FCMDevice, on_delete=models.CASCADE, related_name="receiver_device")
    replay = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

