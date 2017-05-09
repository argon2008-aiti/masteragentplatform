from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views import View
from django.forms import formset_factory
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

from forms import *
from models import *

from utils.models import vending_products, Product
import itertools

class NewBookingView(LoginRequiredMixin, FormView):
    template_name = 'sales/new_booking.html'
    form_class = BookingForm
    login_url = '/login/'

    def get_initial_data(self):
        products = Product.objects.all()
        initial_data = []

        for code in vending_products:
            for p in products:
                if p.code == code:
                    initial_data.append(
                        {'product_id': p.id,
                         'product_code': p.code,
                         'booking': 0,
                         'product_name': p.name})
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
            existing_bookings = VendorBooking.objects.filter(date=booking_form_clean.get('date'))
            vendors = [booking.vendor for booking in existing_bookings.all()]

            if booking_form_clean.get('vendor') in vendors:
                booking_form.add_error('vendor', "This Vendor has already been booked for the day")
                return self.render_to_response(self.get_context_data(formset=formset, booking_form=booking_form))
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
    booking_dates = []


    def get_queryset(self, **kwargs):
        index = self.request.GET.get('page')
        if index==None:
            index = 1
        booking_dates = VendorBooking.objects.annotate(_date=TruncDate('date'))\
                                   .values('date')\
                                   .annotate(Count('id'))
        self.booking_dates = booking_dates
        booking_date = booking_dates[int(index)-1].get('date')
        objects = VendorBooking.objects.filter(date=booking_date)
        sales_dict = {}
        sales_container = []

        sales_dict['date'] = booking_date
        sales_dict['sales'] = objects
        sales_container.append(sales_dict)
        return sales_container

    def get_page_object(self):
        index = self.request.GET.get('page')
        if index==None:
            index=1
        index = int(index)
        total_pages = len(self.booking_dates)
        page_dict = {}
        page_dict['has_previous'] = index > 1
        page_dict['has_next'] = index < total_pages

        page_dict['next_page_number'] = index + 1
        page_dict['previous_page_number'] = index - 1

        page_dict['number'] = index

        return page_dict
        

    def get_context_data(self, **kwargs):
        q_set = self.get_queryset()
        context = super(AllBookingView, self).get_context_data(**kwargs)

        daily_sales_dict = {}

        for sale in q_set[0].get('sales'):
            product_sale_list = []
            for code in vending_products:
                found =0
                for product_booking in sale.productbooking_set.all():
                    if product_booking.product.code == code:
                        product_sale_list.append(product_booking.booking)
                        if sale.closed == True:
                            product_sale_list.append(product_booking.returns)
                            product_sale_list.append(product_booking.booking-product_booking.returns)
                        else:
                            product_sale_list.append(" ")
                            product_sale_list.append(" ")
                        found =1
                        break
                if found==0:
                    product_sale_list.append(" ")
                    product_sale_list.append(" ")
                    product_sale_list.append(" ")

            daily_sales_dict[sale.pk] = product_sale_list

        context['daily_sales_dict']   = daily_sales_dict

        total_pages = len(self.booking_dates)

        if total_pages < 2:
            context['is_paginated'] = False
        else:
            context['is_paginated'] = True
            context['page_range'] = range(1,total_pages+1)
            context['page_obj'] = self.get_page_object()

        return context

class BookingUpdateView(LoginRequiredMixin, FormView):
    template_name = 'sales/new_booking.html'
    form_class = UpdateBookingForm
    login_url ='/login/'
    vendor_booking = None

    def get_context_data(self, **kwargs):
        context = super(BookingUpdateView, self).get_context_data(**kwargs)
        data = {'vendor': self.vendor_booking.vendor.id, 'date': self.vendor_booking.date}

        ProductBookingFormSet = formset_factory(ProductBookingForm, extra=0)

        formset = ProductBookingFormSet(initial=self.get_initial_data())

        booking_form = UpdateBookingForm(initial=data)

        context['formset'] = formset
        context['booking_form'] = booking_form
        return context

    def get_initial_data(self):
        initial_data = [
            {'product_id': productbooking.product.id,
             'product_code': productbooking.product.code,
             'booking': productbooking.booking,
             'product_name': productbooking.product.name} for productbooking in \
                self.vendor_booking.productbooking_set.all()]
        return initial_data

    def get(self, request, *args, **kwargs):
        self.vendor_booking = VendorBooking.objects.get(pk=kwargs.get('pk'))
        context = self.get_context_data()

        if self.vendor_booking.closed == False:
            self.template_name = 'sales/edit_booking.html'

        else:
            self.template_name = 'sales/edit_closed_booking.html'

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.vendor_booking = VendorBooking.objects.get(pk=kwargs.get('pk'))

        ProductBookingFormSet = formset_factory(ProductBookingForm, extra=0)
        formset = ProductBookingFormSet(request.POST)

        if formset.is_valid():
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
                for form in formset:
                    product = Product.objects.get(pk=form.cleaned_data.get('product_id'))
                    product_booking = self.vendor_booking.productbooking_set.get(product=product)
                    new_booking = form.cleaned_data.get('booking')
                    product_booking.booking = new_booking
                    product_booking.save()
        
        return HttpResponseRedirect(reverse('sales:bookings-all'))

class CloseBookingView(LoginRequiredMixin, FormView):
    template_name = 'sales/sales_closure.html'
    form_class = SalesClosureForm
    login_url ='/login/'
    vendor_booking = None

    def get_context_data(self, **kwargs):
        context = super(CloseBookingView, self).get_context_data(**kwargs)
        data = {'vendor': self.vendor_booking.vendor.id, 'date': self.vendor_booking.date}

        SalesClosureFormSet = formset_factory(SalesClosureForm, extra=0)

        formset = SalesClosureFormSet(initial=self.get_initial_data())

        booking_form = UpdateBookingForm(initial=data)

        title = "Close Booking"

        if self.vendor_booking.closed:
            title = "Edit Booking"

        context['formset'] = formset
        context['booking_form'] = booking_form
        context['title'] = title
        return context

    def get_initial_data(self):
        initial_data = [
            {'product_id': productbooking.product.id,
             'product_code': productbooking.product.code,
             'booking': productbooking.booking,
             'returns': productbooking.returns,
             'unit_price': productbooking.product.unit_price,
             'product_name': productbooking.product.name} for productbooking in \
                self.vendor_booking.productbooking_set.all()]
        return initial_data

    def get(self, request, *args, **kwargs):
        self.vendor_booking = VendorBooking.objects.get(pk=kwargs.get('pk'))
        context = self.get_context_data()

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.vendor_booking = VendorBooking.objects.get(pk=kwargs.get('pk'))

        SalesClosureFormSet = formset_factory(SalesClosureForm, extra=0)
        formset = SalesClosureFormSet(request.POST)
        
        if formset.is_valid():
            prod_count = 0
            for form in formset:
                cleaned_data = form.cleaned_data
                if cleaned_data.get('returns')=="":
                    prod_count = prod_count + 1
                else:
                    continue
            if prod_count > 0:
                form.add_error('returns', "returns field cannot be empty")
                return self.render_to_response(self.get_context_data(formset=formset, booking_form=booking_form))
            else:
                total = 0
                for form in formset:
                    product = Product.objects.get(pk=form.cleaned_data.get('product_id'))
                    product_booking = self.vendor_booking.productbooking_set.get(product=product)
                    returns = form.cleaned_data.get('returns')
                    product_booking.returns = returns
                    product_booking.save()
                    total = total + product.unit_price*(product_booking.booking-product_booking.returns)

                self.vendor_booking.closed = True
                self.vendor_booking.total = total
                self.vendor_booking.save()
        
        return HttpResponseRedirect(reverse('sales:bookings-all'))

class BookingsDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/booking_details.html'
    form_class = BookingsDetailForm
    login_url ='/login/'
    vendor_booking = None

    def get_context_data(self, **kwargs):
        context = super(BookingsDetailView, self).get_context_data(**kwargs)
        self.vendor_booking = VendorBooking.objects.get(pk=kwargs.get('pk'))
        data = {'vendor': self.vendor_booking.vendor.id, 'date': self.vendor_booking.date}

        BookingsDetailFormSet = formset_factory(BookingsDetailForm, extra=0)

        formset = BookingsDetailFormSet(initial=self.get_initial_data())

        booking_form = UpdateBookingForm(initial=data)

        context['formset'] = formset
        context['booking_form'] = booking_form
        return context

    def get_initial_data(self):
        initial_data = [
            {'product_id': productbooking.product.id,
             'product_code': productbooking.product.code,
             'booking': productbooking.booking,
             'returns': productbooking.returns,
             'unit_price': productbooking.product.unit_price,
             'product_name': productbooking.product.name} for productbooking in \
                self.vendor_booking.productbooking_set.all()]
        return initial_data

class PayBookingView(LoginRequiredMixin, FormView):
    form_class = BookingPaymentForm
    success_url = '/sales/bookings/all'
    template_name = 'sales/pay_booking.html'

    def get_initial(self):
        v_id = self.kwargs.get('pk')
        initial = super(PayBookingView, self).get_initial()
        initial['vendor'] = VendorBooking.objects.get(pk=v_id).vendor.id
        initial['date'] = VendorBooking.objects.get(pk=v_id).date
        initial['sale_total'] = VendorBooking.objects.get(pk=v_id).total

        return initial

    def form_valid(self, form):
        v_id = self.kwargs.get('pk')
        amount_paid = form.cleaned_data.get('payment_total')
        vendor_booking = VendorBooking.objects.get(pk=v_id)
        vendor_booking.amount_paid = amount_paid
        vendor_booking.paid = True
        vendor_booking.save()
        return super(PayBookingView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PayBookingView, self).form_invalid(form)
