from django import forms

class CheckoutForm(forms.Form):
    stripe_token = forms.CharField()
    amount = forms.IntegerField()
    
class TryForm(forms.Form):
    book_name = forms.CharField()
    amount = forms.IntegerField()