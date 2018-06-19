from django.conf.urls import url
from .views.api import (GetCategories, GetBooks, GetBookDetail, BookSearch, 
                        FilterList, BookFilter, OrdersDetailView, OrdersView)

urlpatterns = [
    url(r'^category-list/$', GetCategories.as_view(), name='category-list'),
    url(r'^book-list/$', GetBooks.as_view(), name='books-list'),
    url(r'^book-detail/$', GetBookDetail.as_view(), name='book-detail'),
    url(r'^search-books/$', BookSearch.as_view(), name='search-books'),
    url(r'^filters/$', FilterList.as_view(), name='filters'),
    url(r'^book-filters/$', BookFilter.as_view(), name='book-filters'),
    url(r'^get-orders/$', OrdersView.as_view(), name='get-orders'),
    url(r'^get-order-detail/$', OrdersDetailView.as_view(), name='get-order-detail'),
]
