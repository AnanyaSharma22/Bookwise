from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.response import Response
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from django.conf import settings
from django.db.models import Q
from bookstore.core.permissions import (PublicTokenAccessPermission,
                                       PrivateTokenAccessPermission,
                                       PublicPrivateTokenAccessPermission)
from catalog.models import Genre, Book, Author, Publisher, Order, OrderDetail
from catalog.serializers import (CategoryListingSerializer, BooksListingSerializer,
                                 BookDetailSerializer, AuthorSerializer,
                                 PublisherSerializer,
                                 OrdersViewSerializer, OrdersDetailViewSerializer)

class CategoryRecordsPagination(PageNumberPagination):
    ''' Record Pagination '''
    page_size = settings.GET_CATEGORY_API_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class GetCategories(generics.ListAPIView):
    '''
    Get all categories listing
    '''
    serializer_class = CategoryListingSerializer
    permission_classes = (PrivateTokenAccessPermission, )
    def get_queryset(self):
        queryset = Genre.objects.filter().order_by('name')
        return queryset

class GetBooks(generics.ListAPIView):
    '''
    Get all Books Listing
    '''
    serializer_class = BooksListingSerializer
    pagination_class = CategoryRecordsPagination
    permission_classes = (PrivateTokenAccessPermission, )
    def get_queryset(self):
        genre_id = self.request.query_params['genre_id']
        queryset = Book.objects.filter(genre=genre_id).order_by('title')
        return queryset

class GetBookDetail(generics.RetrieveAPIView):
    serializer_class = BookDetailSerializer
    permission_classes = (PrivateTokenAccessPermission, )
    def get_object(self):
        book_id = self.request.query_params['book_id']
        queryset = Book.objects.filter(id=book_id).first()
        return queryset

class BookSearch(generics.ListAPIView):
    serializer_class = BooksListingSerializer
    pagination_class = CategoryRecordsPagination
    permission_classes = (PrivateTokenAccessPermission, )
    def get_queryset(self):
        genre_id = self.request.query_params['genre_id']
        search_text = self.request.query_params['search_text']
        query = Q(title__icontains=search_text) | Q(author__name__icontains=search_text)
        queryset = Book.objects.filter(genre=genre_id).filter(query)
        return queryset

class FilterList(ObjectMultipleModelAPIView):
    querylist = (
        {'queryset':Genre.objects.all(), 'serializer_class':CategoryListingSerializer},
        {'queryset':Author.objects.all(), 'serializer_class':AuthorSerializer},
        {'queryset':Publisher.objects.all(), 'serializer_class':PublisherSerializer},
    )   
    pagination_class = CategoryRecordsPagination
    permission_classes = (PrivateTokenAccessPermission, )

class BookFilter(generics.ListAPIView):
    # queryset = Book.objects.all()
    pagination_class = CategoryRecordsPagination
    serializer_class = BooksListingSerializer
    permission_classes = (PrivateTokenAccessPermission, )
    def get_filters(self, request):
        genres = self.request.query_params.get('genres', None)
        authors = self.request.query_params.get('authors', None)
        publishers = self.request.query_params.get('publishers', None)
        price_start = self.request.query_params.get('start', None)
        price_end = self.request.query_params.get('end', None)
        if price_start:
            price_start = float(price_start)
        if price_end:
            price_end = float(price_end)
        return genres, authors, publishers, price_start, price_end
    def filter_by_authors(self, authors, data):
        '''
        Filter By author
        '''
        authors = authors.split(',')
        return data.filter(author__name__in=authors)

    def filter_by_publishers(self, publishers, data):
        publishers = publishers.split(',')
        return data.filter(publisher__name__in=publishers)

    def filter_by_genres(self, genres, data):
        genres = genres.split(',')
        return data.filter(genre__name__in=genres)

    def filter_by_price_range(self, price_start, price_end, data):
        '''
        Filter By Price Range
        '''
        return data.filter(Q(price__lt=price_end) & Q(price__gte=price_start))

    def get_queryset(self):
        genres, authors, publishers, price_start, price_end = self.get_filters(self.request)
        data = Book.objects.all()
        if genres:
            data = self.filter_by_genres(genres, data)
        if authors:
            data = self.filter_by_authors(authors, data)
        if publishers:
            data = self.filter_by_publishers(publishers, data)
        if price_start != '' and price_start >= 0 and price_end != '':
            data = self.filter_by_price_range(price_start, price_end, data)
        return data

class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrdersViewSerializer
    permission_classes = (PrivateTokenAccessPermission,)

    def get_queryset(self):
        customer = self.request.query_params['customer']
        queryset = Order.objects.filter(customer=customer)
        return queryset

class OrdersDetailView(generics.ListAPIView):
    serializer_class = OrdersDetailViewSerializer
    permission_classes = (PrivateTokenAccessPermission,)

    def get_queryset(self):
        order_id = self.request.query_params['order_id']
        queryset = OrderDetail.objects.filter(order_id=order_id)
        return queryset
