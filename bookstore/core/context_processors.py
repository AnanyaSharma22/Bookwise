from catalog.models import Book

def latest_books(self):
    latest = Book.objects.all().order_by('-added_date')[:8]
    return {'latest': latest}
