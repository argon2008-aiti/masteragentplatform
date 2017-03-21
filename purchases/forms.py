from django import forms
from models import PAYMENT_TYPE, PURCHASE_TYPE

class ProductPurchaseForm(forms.Form):
    product_id = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=20)
    product_code = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=20)
    product_name = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=100)
    unit_price = forms.FloatField(required=False, widget=forms.HiddenInput())
    quantity = forms.IntegerField()

class DayPurchaseForm(forms.Form):
    invoice_number = forms.CharField(max_length=20);
    purchase_date = forms.DateField(input_formats=('%d-%m-%Y',))
    purchase_type = forms.ChoiceField(choices=PURCHASE_TYPE)
    payment_option = forms.ChoiceField(choices=PAYMENT_TYPE)

    issuing_bank = forms.CharField(required=False, max_length=50)
    account_number = forms.CharField(required=False, max_length=20)
    cheque_number = forms.CharField(required=False, max_length=10)
    cheque_date = forms.DateField(required=False, input_formats=('%d-%m-%Y',))
    amount_on_cheque = forms.FloatField(required=False)

    total_cash = forms.FloatField(required=False)
    
class PaymentForm(forms.Form):
    payment_option = forms.ChoiceField(choices=PAYMENT_TYPE)

    issuing_bank = forms.CharField(required=False, max_length=50)
    account_number = forms.CharField(required=False, max_length=20)
    cheque_number = forms.CharField(required=False, max_length=10)
    cheque_date = forms.DateField(required=False, input_formats=('%d-%m-%Y',))
    amount_on_cheque = forms.FloatField(required=False)

    total_cash = forms.FloatField(required=False)
    
