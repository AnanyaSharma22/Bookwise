from rest_framework import serializers
from catalog.models import Genre, Book, Author, Publisher, Order, OrderDetail

class CategoryListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']

class BooksListingSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, many=True)
    publisher = serializers.ReadOnlyField(source='publisher.name')
    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'genre', 'publisher', 'author', 'image')

class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, many=True)
    publisher = serializers.ReadOnlyField(source='publisher.name')
    genre = serializers.ReadOnlyField(source='genre.name')
    class Meta:
        model = Book
        fields = ('isbn', 'id', 'title', 'description', 'author', 'publisher', 'publication_date', 'image', 'pages', 'price', 'genre')

class OrdersDetailViewSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(source='bk_id', read_only=True)
    class Meta(object):
        model = OrderDetail
        fields = ('bk_id', 'qty', 'price','book')

class OrdersViewSerializer(serializers.ModelSerializer):
    order_id = OrdersDetailViewSerializer(many=True)
    class Meta(object):
        model = Order
        fields = ('customer', 'stripe_cust_id', 'total_amt', 'order_date', 'order_time', 'order_id')
    def create(self, validated_data):
        order_data = validated_data.pop('order_id')
        order = Order.objects.create(**validated_data)
        for order_detail in order_data:
            OrderDetail.objects.create(order_id=order, **order_detail)
        return order