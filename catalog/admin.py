from django.conf import settings
from django.contrib import admin
from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.admin import SimpleListFilter
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from app.models import EmailMessage

from .models import Author, Book, Genre, Publisher, Review, Order, OrderDetail

# Register your models here.

class RemoveAdd(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

class ReviewAdmin(RemoveAdd):
    pass

class AuthorAdmin(admin.ModelAdmin):
    fields = ['name','description']
    

class GenreAdmin(admin.ModelAdmin):
    fields = ['title',]
  

class PublisherAdmin(admin.ModelAdmin):
    fields = ['name','address',]

class StockListFilter(SimpleListFilter):
    title = 'In Stock' 
    parameter_name = 'stock_free'
    def lookups(self, request, model_admin):
        return (
            ('0', 'Yes', ),
            ('1', 'No', ),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            result = queryset.filter(stock_free=False)
        elif self.value() == '1':
            result = queryset.filter(stock_free=True)
        else:
            result = queryset
        return result

class BookAdmin(admin.ModelAdmin):
    list_display = ['isbn', 'title', 'in_stock', 'genre', 'status', 'avg_rating']
    ordering = ['title']
    actions = ['make_published','delete_books']
    search_fields = ['title']
    autocomplete_fields = ['Author']
    fieldsets = (
        ('', {
            'fields': ('isbn','title','description','image')
        }),
        ('Author/Publisher', {
            'fields': ('author','publisher','publication_date','genre')
        }),        
        ('Meta Data', {
            'fields': ('pages','price','stock_free','stock_qty','free_delivery','status', 'avg_rating')
        }),
    )
    readonly_fields = ['avg_rating']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected books as published"
    
    def delete_books(self, request, queryset):
        queryset.update(is_active=False)
    delete_books.short_description = "Mark selected books to be deleted"

    def in_stock(self, obj):
            return 'No' if obj.stock_free else 'Yes'

# in_stock.short_description = 'In Stock'
    list_filter = (
        (StockListFilter,)
    )


    # list_filter = (
    #     ('is_active', admin.BooleanFieldListFilter),
    # )
    # list_filter = (
    #     ('genre'),
    # ) 
    # list_filter = (
    #     ('is_active', admin.BooleanFieldListFilter),
    # )
class OrderAdmin(RemoveAdd):

    list_display = ['order_id','bk_id','qty','price',]

    def has_add_permission(self, request):
        return False

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return super(FlatPageAdmin, self).get_readonly_fields(request, obj)
        else:
            return ('url')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('url',)
        return self.readonly_fields

# Re-register FlatPageAdmin
if not settings.DEBUG:
    admin.site.unregister(AccessToken)
    admin.site.unregister(Application)
    admin.site.unregister(Grant)
    admin.site.unregister(RefreshToken)
    admin.site.unregister(Group)
    admin.site.unregister(Site)
    admin.site.unregister(EmailMessage)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order,RemoveAdd)
admin.site.register(OrderDetail, OrderAdmin)
