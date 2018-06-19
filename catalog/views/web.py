import stripe
import json
import copy

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Min, Max
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import ContactUs, Address
from catalog.filters import CatalogFilter
from catalog.models import Book, Genre, Author, Publisher, OrderDetail, Order, Review
from catalog.forms import CheckoutForm, TryForm
from django.shortcuts import get_object_or_404

def insert_order(self):
    data={}
    user=self.request.user
    total_amount = self.request.POST['total_amount']
    order = Order.objects.create(customer=user, total_amt=total_amount)
    book_data = json.loads(self.request.POST.get('book_data'))
    for book in book_data :
        book_obj=Book.objects.get(pk=book['id'])
        orderdetail = OrderDetail.objects.create(order_id=order, bk_id=book_obj, qty=book['quantity'], price=book['price'])
    data['success'] = "Your Order has been Placed Successfully"
    data['target_url'] = reverse('catalog:order-detail',kwargs={'id':order.id})
    return data

class HomeView(TemplateView):
    template_name = 'layouts/index.html'


class AboutView(TemplateView):
    template_name = 'layouts/about.html'


class BookDetailView(TemplateView):

    template_name = 'layouts/single_product.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['book'] = get_object_or_404(
            Book, slug__iexact=self.kwargs['Book_slug'])
        rating = Review.objects.filter(book=context['book']).order_by(
            'id').select_related('customer')
        rating_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'total': 0}
        for i in range(rating.count()):
            rate = rating[i].rating
            rating_total[rate] = rating_total[rate] + 1
            rating_total['total'] = rating_total['total'] + 1
            customer = rating[i].customer.email
            if not self.request.user.is_anonymous() and self.request.user.email == customer:
                context['userreview'] = rating[i]

        context['ratings'] = rating
        context['rating_total'] = rating_total
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            post_data = request.POST
            user = request.user
            book = Book.objects.get(pk=post_data.get('book_id'))
            Review.objects.update_or_create(
                customer=user,
                book=book,
                defaults={'rating': post_data.get(
                    'rating'), 'comment': post_data.get('comment')},
            )
            return HttpResponseRedirect(request.path_info)


class ContactView(TemplateView):
    template_name = 'layouts/contact.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            user = self.request.user
        else:
            user = None
        contact_instance = ContactUs(
            # user=self.request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            message=request.POST['message']
        )
        contact_instance.save()
        ContactUs.contact_us_email(request, contact_instance)
        return HttpResponseRedirect(reverse_lazy('catalog:home'))


@method_decorator(csrf_exempt, name='dispatch')
class CheckOutView(LoginRequiredMixin, FormView):
    template_name = 'layouts/checkout.html'
    form_class = TryForm

    def get_context_data(self, **kwargs):
        context = super(CheckOutView, self).get_context_data(**kwargs)
        user_address = Address.objects.filter(user=self.request.user)
        if user_address:
            context['address'] = user_address[0]
        return context

class OrderSuccess(FormView):
    template_name = 'layouts/success.html'
    form_class = CheckoutForm


class PaymentView(LoginRequiredMixin, FormView):
    template_name = 'layouts/payment.html'
    form_class = CheckoutForm

    def dispatch(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return super(PaymentView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('catalog:checkout'))

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            user = self.request.user
            user_data = self.request.POST
            landmark = user_data.get('area')
            city = user_data.get('city')
            state = user_data.get('state')
            country = user_data.get('country')
            house = user_data.get('house')
            pincode = user_data.get('pincode')

            obj, created = Address.objects.update_or_create(
                user=user,
                defaults={'landmark': landmark, 'city': city, 'state': state,
                          'house_no': house, 'country': country, 'pincode': pincode},
            )
            # context['payment_amount'] = self.request.POST.get('amount')

            context['publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge_view(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    token = request.POST.get('stripeToken')

    charge = stripe.Charge.create(
        amount=100000,
        currency='inr',
        description='Example charge from view',
        source=token,
    )

    from django.http import HttpResponse
    return HttpResponse('<h1>Success</h1>')


class OrderView(ListView):
    model = Order
    template_name = 'layouts/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        user = self.request.user
        context['object_list'] = Order.objects.filter(customer=user.id)
        return context


class OrderDetailView(TemplateView):

    template_name = 'layouts/order_detail.html'

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order_list'] = OrderDetail.objects.filter(
            order_id=self.kwargs['id'])
        return context


class FaqView(TemplateView):
    template_name = 'layouts/faq.html'


class SearchView(ListView):
    '''
    Search View
    '''
    template_name = 'layouts/search.html'

    def get_queryset(self):
        keywords = self.request.GET.get('q')
        if keywords:
            queryset = Book.objects.filter(Q(title__icontains=keywords) | Q(description__icontains=keywords) | Q(
                author__name__icontains=keywords) | Q(publisher__name__icontains=keywords) | Q(genre__name__icontains=keywords)).prefetch_related('author')
            return queryset
        else:
            queryset = 'No context'
            return queryset

class FaqView(TemplateView):
    template_name = 'layouts/faq.html'

@method_decorator(csrf_exempt, name='dispatch')
class PaymentCOD(CreateView):

    template_name = 'layouts/shop.html'

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        if self.request.is_ajax():
            try:
                data = insert_order(self)
            except ObjectDoesNotExist:
                data['error'] = "There was a problem while placing your order"
            
            result=json.dumps(data)

        return HttpResponse(result, content_type="application/json")

