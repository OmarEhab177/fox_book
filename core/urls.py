# from django.urls import path, include
from urllib.parse import urlparse
from rest_framework.routers import DefaultRouter
from .views import (BooksListMethod, BookCategoryMethod, BookCollectionMethod, BookFavorites, BookFavoriteList,
BookPagesMethod, PageFavorites, PageFavoriteList, LibsMethod)

router = DefaultRouter(trailing_slash=False)
router.register('books', BooksListMethod)
router.register('book_category', BookCategoryMethod)
router.register('book_collection', BookCollectionMethod)
router.register('book_favorite/(?P<pk>\d+)/?$', BookFavorites)
router.register('book_favorites', BookFavoriteList)
router.register('book_pages', BookPagesMethod)
router.register('page_favorite/(?P<pk>\d+)/?$', PageFavorites)
router.register('page_favorites', PageFavoriteList)
router.register('add_libs', LibsMethod)
urlpatterns = router.urls


