from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.forms import formset_factory

from forms import *
from models import *

from utils.models import vending_products, Product

class NewBookingView(LoginRequiredMixin, FormView):
    template_name = 'sales/new_booking.html'
    form_class = BookingForm
    login_url = '/login/'

    def get_initial_data(self):
        products = Product.objects.all()
        initial_data = [
            {'product_id': product.id,
             'product_code': product.code,
             'booking': 0,
             'product_name': product.name} for product in products if product.code in vending_products]
        return initial_data
    

    def get(self, request, *args, **kwargs):
        ProductBookingFormSet = formset_factory(ProductBookingForm, extra=0)
        booking_form = BookingForm()

        formset = ProductBookingFormSet(initial=self.get_initial_data())
        return self.render_to_response(self.get_context_data(formset=formset, booking_form=booking_form))

    def post(self, request, *args, **kwargs):
        booking_form = BookingForm(request.POST)

        ProductBookingFormSet = formset_factory(ProductBookingForm, extra=0)
        formset = ProductBookingFormSet(request.POST)

        if booking_form.is_valid() and formset.is_valid():
            booking_form_clean = booking_form.cleaned_data
            vendor_booking = VendorBooking()
            vendor_booking.date = booking_form_clean.get('date')
            vendor_booking.vendor = booking_form_clean.get('vendor')

            prod_count = 0
            for form in formset:
                cleaned_data = form.cleaned_data
                if cleaned_data.get('booking')==0 or cleaned_data.get('booking')=="":
                    continue
                else:
                    prod_count = prod_count + 1
            if prod_count == 0:
                form.add_error('booking', "At least one product must have a booking greater than 0")
                return self.render_to_response(self.get_context_data(formset=formset, booking_form=booking_form))
            else:
                vendor_booking.save()
                for form in formset:
                    product_booking = ProductBooking()
                    product_booking.booking = form.cleaned_data.get('booking')
                    product_booking.product = Product.objects.get(pk=form.cleaned_data.get('product_id'))
                    product_booking.master_booking = vendor_booking
                    product_booking.save()
            return HttpResponseRedirect(reverse('sales:bookings-all'))
        
        else:
            return self.render_to_response(self.get_context_data(formset=formset, booking_form=booking_form))

class AllBookingView(LoginRequiredMixin, ListView):
    template_name = 'sales/all_booking.html'
    model = VendorBooking
    login_url = '/login/'

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'sales/update_booking.html'
    form_class = UpdateBookingForm
    login_url ='/login/'

    def get_initial_data(self):
        vendor_booking = self.get_object()
        initial_data = [
            {'product_id': productbooking.product.id,
             'product_code': productbooking.product.code,
             'booking': productbooking.booking,
             'product_name': productbooking.product.name} for productbooking in \
                vendor_booking.productbooking_set.all()]
        return initial_data
