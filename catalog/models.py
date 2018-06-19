import datetime
import itertools
from unidecode import unidecode
from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Avg
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Genre (models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def save(self, *args, **kwargs):
        if not self.slug:
            lenslug = 210
            sludata = unidecode(self.name)
            if not len(sludata) > 210:
                lenslug = len(sludata)
            sludata = slugify(sludata)[0:lenslug]
            self.slug = sludata
            for list_iter in itertools.count(1):
                if not Genre.objects.filter(slug__iexact=sludata).exists():
                    break
                sludata = "%s-%d" % (slugify(self.slug), list_iter)
            self.slug = sludata
        return super(Genre, self).save(*args, **kwargs)

class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def save(self, *args, **kwargs):
        if not self.slug:
            lenslug = 210
            sludata = unidecode(self.name)
            if not len(sludata) > 210:
                lenslug = len(sludata)
            sludata = slugify(sludata)[0:lenslug]
            self.slug = sludata
            for list_iter in itertools.count(1):
                if not Author.objects.filter(slug__iexact=sludata).exists():
                    break
                sludata = "%s-%d" % (slugify(self.slug), list_iter)
            self.slug = sludata
        return super(Author, self).save(*args, **kwargs)

class Publisher(models.Model):
    name = models.CharField('Name', max_length=244)
    address = models.TextField(null=True, blank=True, max_length=150)
    slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def save(self, *args, **kwargs):
        if not self.slug:
            lenslug = 210
            sludata = unidecode(self.name)
            if not len(sludata) > 210:
                lenslug = len(sludata)
            sludata = slugify(sludata)[0:lenslug]
            self.slug = sludata
            for list_iter in itertools.count(1):
                if not Publisher.objects.filter(slug__iexact=sludata).exists():
                    break
                sludata = "%s-%d" % (slugify(self.slug), list_iter)
            self.slug = sludata
        return super(Publisher, self).save(*args, **kwargs)

class Book(models.Model):
    p_choices = (
        ('published', 'Published'),
        ('pending', 'Pending'),
    )
    isbn = models.CharField(max_length=16)
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ManyToManyField(Author)
    status = models.CharField(choices=p_choices, max_length=20)
    is_featured = models.BooleanField(default=False)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    image = models.ImageField(null=True, blank= True, upload_to='books/')
    pages = models.IntegerField()
    price = models.IntegerField()
    genre = models.ForeignKey(Genre)
    stock_qty = models.IntegerField('Available Stock', default=0)
    stock_free = models.BooleanField(default=True)
    free_delivery = models.BooleanField(default=False)
    slug = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    avg_rating = models.FloatField(blank=True, null= True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


    def save(self, *args, **kwargs):
        if not self.slug:
            lenslug = 210
            sludata = u'-'.join([unidecode(self.isbn) , unidecode(self.title)])
            if not len(sludata) > 210:
                lenslug = len(sludata)
            sludata = slugify(sludata)[0:lenslug]
            self.slug = sludata
            for list_iter in itertools.count(1):
                if not Book.objects.filter(slug__iexact=sludata).exists():
                    break
                sludata = "%s-%d" % (slugify(self.slug), list_iter)
            self.slug = sludata
        
        if self.image:           
            im = Image.open(self.image)
            output = BytesIO()
            #Resize/modify the image
            im = im.resize( (200,300) )
            #after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)
            #change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        return super(Book, self).save(*args, **kwargs)


class Review(models.Model):
    '''
    model for book Review
    '''
    book = models.ForeignKey(Book, related_name='book')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='customer')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    rating = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    comment = models.TextField(null=True, blank = True)

    class Meta:
        unique_together = (('book', 'customer'),)

    def __str__(self):
        return '%s rated %s by %s' % (self.book, self.rating , self.customer)


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_book_rating(sender, **kwargs):
    if kwargs:
        book = kwargs['instance'].book
        avg_rating = Review.objects.filter(book = book).aggregate(Avg('rating'))
        book_rating = avg_rating['rating__avg']
        Book.objects.filter(id = book.id).update(avg_rating = book_rating)
    
class Order(models.Model):
    order_choices = (
        ('dispatched', 'dispatched'),
        ('delivered', 'Delivered'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='cust')
    stripe_cust_id = models.CharField(max_length=50, blank=True, null=True)
    total_amt = models.IntegerField()
    order_date = models.DateField(default=datetime.date.today)
    order_time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    status = models.CharField(choices=order_choices, max_length=30, default='dispatched')

    def __str__(self):
        return '{0}'.format(self.customer)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderDetail(models.Model):
    order_id = models.ForeignKey(Order, related_name='order_id')
    bk_id = models.ForeignKey(Book, related_name='bk_id')
    qty = models.IntegerField(default=0)
    price = models.IntegerField()

    def __str__(self):
        return '{0}'.format(self.order_id)

    class Meta:
        verbose_name = 'OrderDetail'
        verbose_name_plural = 'OrderDetails'