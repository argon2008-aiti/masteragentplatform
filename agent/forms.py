from django import forms
from models import Vendor
from agent.models import ShopAssistant


class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ['first_name', 'last_name', 'phone', 'hometown',
                  'guarantor', 'relation', 'guarantor_phone',
                  'guarantor_location', 'date_of_birth', 'profile']
