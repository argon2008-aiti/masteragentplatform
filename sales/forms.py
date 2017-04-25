from django import forms
from agent.models import Vendor

class BookingForm(forms.Form):
    vendor = forms.ModelChoiceField(Vendor.objects.all())
    date   = forms.DateField(input_formats=('%d-%m-%Y',))

class UpdateBookingForm(forms.Form):
    vendor = forms.ModelChoiceField(Vendor.objects.all(), disabled=True)
    date   = forms.DateField(input_formats=('%d-%m-%Y',), disabled=True)

class ProductBookingForm(forms.Form):
    product_id = forms.CharField(required=False, widget=forms.HiddenInput()) 
    product_name = forms.CharField(required=False, widget=forms.HiddenInput()) 
    product_code = forms.CharField(required=False, widget=forms.HiddenInput()) 
    booking    = forms.IntegerField(min_value=0)

class SalesClosureForm(forms.Form):
    product_id = forms.CharField(required=False, widget=forms.HiddenInput()) 
    product_name = forms.CharField(required=False, widget=forms.HiddenInput()) 
    product_code = forms.CharField(required=False, widget=forms.HiddenInput()) 
    unit_price = forms.CharField(required=False, widget=forms.HiddenInput()) 
    booking    = forms.IntegerField(min_value=0, required=False, disabled=True)
    returns    = forms.IntegerField(min_value=0)

class BookingPaymentForm(forms.Form):
    vendor = forms.ModelChoiceField(Vendor.objects.all(), required=False, disabled=True)
    date   = forms.DateField(input_formats=('%d-%m-%Y',), required=False, disabled=True)
    sale_total = forms.FloatField(required=False, disabled=True)
    payment_total = forms.FloatField(min_value=0.0)

