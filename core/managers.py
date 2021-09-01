from django.db import models

class TodayBooks(models.Manager):
    def get_queryset(self):
        return super(TodayBooks, self).get_queryset().filter(is_active=True).filter(is_today=True).order_by('-created_at')

class RecentBook(models.Manager):
    def get_queryset(self):
        return super(RecentBook, self).get_queryset().filter(is_active=True).filter(is_recent_books=True).order_by('-created_at')

class Last10Books(models.Manager):
    def get_queryset(self):
        return super(Last10Books, self).get_queryset().filter(is_active=True).order_by('-created_at')[:2]
        