from django.contrib import admin
from .models import User, Address, ContactUs
# Register your models here.
class RemoveAdd(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

class ContactUsAdmin(RemoveAdd):
    list_display = ['first_name', 'last_name', 'email', 'message']

admin.site.register(User, RemoveAdd)
admin.site.register(Address,RemoveAdd)
admin.site.register(ContactUs, ContactUsAdmin)

