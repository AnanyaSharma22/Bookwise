from django.conf.urls import url, include
from django_filters.views import FilterView
from catalog.filters import CatalogFilter
from catalog.views.web import (HomeView, AboutView, BookDetailView, ContactView, 
                              CheckOutView, PaymentView, OrderSuccess, 
                              charge_view, OrderView, OrderDetailView, FaqView,
                              SearchView, PaymentCOD)
app_name = 'catalog'
urlpatterns = [
    url(r'^$', HomeView.as_view() , name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^shop/$', FilterView.as_view(filterset_class=CatalogFilter,
        template_name='layouts/shop.html'), name='shop'),
    url(r'^shop/(?P<Book_slug>[\w-]+)/$', BookDetailView.as_view(), name='book-detail'),
    url(r'^checkout/$', CheckOutView.as_view(), name='checkout'),
    url(r'^payment/$', PaymentView.as_view(), name='payment'),
    url(r'^order-success/$', OrderSuccess.as_view(), name='success'),
    url(r'^charge/$', charge_view, name= 'charge'),
    url(r'^cod/$', PaymentCOD.as_view(), name='cod'),
    url(r'^order-list/$', OrderView.as_view(), name='order'),
    url(r'^order-list/(?P<id>[0-9]+)/$', OrderDetailView.as_view(), name='order-detail'),
    url(r'^faq/$', FaqView.as_view(), name='faq'),
    url(r'^search/$', SearchView.as_view(), name='search-books'),
]
