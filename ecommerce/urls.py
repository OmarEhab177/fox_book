from django.urls import path
from ecommerce import views
urlpatterns = [
    # Ecommerce
    path('products',views.ProductsView.as_view(),name='ecommerce-products'),# Products
    path('product-details/',views.ProductDetailsView.as_view(),name='ecommerce-product-detail'),# Product Details (?P<pk>[0-9]+)/$
    path('book-details/<int:pk>',views.BookDetailsView.as_view(),name='ecommerce-book-detail'),# Product Details (?P<pk>[0-9]+)/$
    path('orders',views.OrdersView.as_view(),name='ecommerce-orders'),# Orders
    path('customers',views.CustomersView.as_view(),name='ecommerce-customers'),# Cusomers
    path('cart',views.CartView.as_view(),name='ecommerce-cart'),# Cart
    path('check-out',views.CheckoutView.as_view(),name='ecommerce-checkout'),# Checkout
    path('shops',views.ShopsView.as_view(),name='ecommerce-shops'),# Shops
    path('add-product',views.AddProductView.as_view(),name='ecommerce-add-product'),# Shops
    path('add-book/', views.AddBookView.as_view(), name='ecommerce-add-book'), 
    path('edit-book/<int:pk>', views.update_book, name='ecommerce-edit-book'), 
    path('delete-book/<int:pk>', views.delete_book, name='ecommerce-delete-book'), 
    path('categories',views.CategoriesViews.as_view(),name='ecommerce-categories'),# Categories
    path('category-details/<int:pk>',views.CategoryDetail.as_view(),name='ecommerce-category-detail'),# Product Details (?P<pk>[0-9]+)/$
    path('add-category/', views.add_category, name='ecommerce-add-category'), 
    path('edit-category/<int:pk>', views.update_category, name='ecommerce-edit-category'),
    path('delete-category/<int:pk>', views.delete_category, name='ecommerce-delete-category'), 
    path('book-categories',views.BookCategoriesView.as_view(),name='ecommerce-book_categories'),# Categories
    path('book-category-details/<int:pk>',views.BookCategoryDetail.as_view(),name='ecommerce-book-category-detail'),# Product Details (?P<pk>[0-9]+)/$
    path('add-book-category/', views.add_book_category, name='ecommerce-add-book-category'), 
    path('add-book-to-category/<int:pk>', views.add_bookToCategory, name='ecommerce-add-book-to-category'), 
    path('edit-book-category/<int:pk>', views.update_book_category, name='ecommerce-edit-book-category'),
    path('delete-book-category/<int:pk>', views.delete_book_category, name='ecommerce-delete-book-category'), 
    path('add-page', views.add_page, name='ecommerce-add-page'), 
    path('edit-page/<int:pk>', views.update_page, name='ecommerce-edit-page'), 
    path('delete-page/<int:pk>', views.delete_page, name='ecommerce-delete-page'), 
    path('page-detail/<int:pk>', views.retrieve_page, name='ecommerce-page-detail'), 
    path('add-book-page', views.add_book_page, name='ecommerce-add-book-page'), 
    path('add-page-to-book/<int:pk>', views.add__page_to_book, name='ecommerce-add-page-to-book'), 
    path('add-pageToBook/<int:pk>', views.add_pageTOBook, name='ecommerce-add-pageToBook'), 
    path('add-collection', views.add_collection, name='ecommerce-add-collection'), 
    path('collections', views.collection_list, name='ecommerce-collections'), 
    path('collection-detail/<int:pk>', views.collection_detail, name='ecommerce-collection-detail'), 
    path('edit-collection/<int:pk>', views.update_collection, name='ecommerce-edit-collection'), 
    path('delete-collection/<int:pk>', views.delete_collection, name='ecommerce-delete-collection'), 
    path('add-bookToCollection/<int:pk>', views.add_bookToCollection, name='ecommerce-add-bookToCollection'), 
    path('add-book-collection', views.add_book_collection, name='ecommerce-add-book-collection'), 
    path('add-book-to-collection/<int:pk>', views.add_book_to_collection, name='ecommerce-add-book-to-collection'), 
    path('add-collection-to-book/<int:pk>', views.add_collection_to_book, name='ecommerce-add-collection-to-book'), 
    path('book-collections', views.book_collection_list, name='ecommerce-book-collections'), 
    path('edit-book-collection/<int:pk>', views.update_book_collection, name='ecommerce-edit-book-collection'), 
    path('delete-book-collection/<int:pk>', views.delete_book_collection, name='ecommerce-delete-book-collection'), 
    path('conatcts-list', views.contacts_list, name='ecommerce-conatcts-list'),
    path('contact-detail/<int:pk>', views.contact_detail, name='ecommerce-contact-detail'), 
    path('delete-contact/<int:pk>', views.delete_contact, name='ecommerce-delete-contact'), 
    path('conatct-replies-list', views.contact_replies_list, name='ecommerce-conatct-replies-list'),
    path('contact-replay-detail/<int:pk>', views.contact_replay_detail, name='ecommerce-contact-replay-detail'), 
    path('add-contact-replay/<int:pk>', views.add_contact_replay, name='ecommerce-add-contact-replay'), 
    path('delete-contact-replay/<int:pk>', views.delete_contact_replay, name='ecommerce-delete-contact-replay'), 
    path('add-tag', views.add_tag, name='ecommerce-add-tag'),
    path('tags', views.tag_list, name='ecommerce-tag-list'),
    path('tag-detail/<int:pk>', views.tag_detail, name='ecommerce-tag-detail'),
    path('delete-tag/<int:pk>', views.delete_tag, name='ecommerce-delete-tag'),
    path('update-tag/<int:pk>', views.update_tag, name='ecommerce-update-tag'),

]
