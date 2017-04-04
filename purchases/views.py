from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from utils.models import Product
from purchases.forms import ProductPurchaseForm, DayPurchaseForm, PaymentForm
from django.forms import formset_factory
from purchases.models import *

import calendar

class NewPurchaseView(LoginRequiredMixin, FormView):
    template_name = 'purchases/new_purchase.html'
    form_class = ProductPurchaseForm
    login_url = '/login/'
    
    def get_initial_data(self):
        products = Product.objects.all()
        product_count = products.count()
        initial_data = [
            {'product_id': product.id, 
             'product_code': product.code, 
             'product_name': product.name,
             'unit_price': product.unit_price,
             'quantity': 0} for product in products]
        return initial_data

    def get(self, request, *args, **kwargs):
        ProductPurchaseFormSet = formset_factory(ProductPurchaseForm, extra=0)
        purchase_form = DayPurchaseForm()
        formset = ProductPurchaseFormSet(initial=self.get_initial_data())
        return self.render_to_response(self.get_context_data(formset=formset, purchase_form=purchase_form))

    def post(self, request, *args, **kwargs):
        ProductPurchaseFormSet = formset_factory(ProductPurchaseForm, extra=0)
        purchase_form = DayPurchaseForm(request.POST)
        formset = ProductPurchaseFormSet(request.POST)
        # only called when form is valid with invoice_number, date and purchase_type provided
        if purchase_form.is_valid():
            cleaned_data = purchase_form.cleaned_data
            purchase_type = cleaned_data.get('purchase_type')
            if purchase_type == '1':
                payment_option = cleaned_data.get('payment_option')
                if payment_option == '0':
                    if check_cheque(purchase_form) == True:
                        return self.form_invalid(formset, purchase_form)
        if formset.is_valid():
            print "problem with form"
            from agent.models import ShopAssistant
            shop = ''
            if 'shopassistants' in [group.name for group in request.user.groups.all()]:
                shop = ShopAssistant.objects.get(user=request.user).shop
            elif u'agents' in [group.name for group in request.user.groups.all()]:
                shop = user.agent.shop
            prod_count = 0
            for form in formset:
                cleaned_data = form.cleaned_data
                if cleaned_data.get('quantity')==0 or cleaned_data.get('quantity') == "":
                    continue
                else:
                    prod_count = prod_count + 1
            if prod_count == 0:
                form.add_error('quantity', "At least one Product must have a quantity greater than 0")
                return self.form_invalid(formset, purchase_form) 
            # Everything is alright.... Begin saving.
            else: 
                day_purchase = DayPurchase()
                day_purchase.shop = shop
                day_purchase.invoice_number = purchase_form.cleaned_data.get('invoice_number')
                purchase_type = purchase_form.cleaned_data.get('purchase_type')
                day_purchase.date = purchase_form.cleaned_data.get('purchase_date')
                day_purchase.purchase_type = purchase_type
                #CREDIT
                if purchase_type == '0':
                    day_purchase.save()
                #CASH
                else:
                    payment_option = purchase_form.cleaned_data.get('payment_option')
                    payment = ProductPayment()
                    payment.payment_type = payment_option

                    #CASH
                    if payment_option == '1':
                        payment.amount_paid  =  purchase_form.cleaned_data.get('total_cash')

                    #CHEQUE
                    else:
                        cheque = Cheque()
                        cheque.bank = purchase_form.cleaned_data.get('issuing_bank')
                        cheque.account_number = purchase_form.cleaned_data.get('account_number')
                        cheque.cheque_number = purchase_form.cleaned_data.get('cheque_number')
                        cheque.cheque_date = purchase_form.cleaned_data.get('cheque_date')
                        cheque.save()
                        payment.cheque = cheque
                        payment.amount_paid = purchase_form.cleaned_data.get('amount_on_cheque')
                    payment.save()
                    day_purchase.payment = payment
                    day_purchase.save()

                for form in formset:
                    # No quantity
                    cleaned_data = form.cleaned_data
                    if cleaned_data.get('quantity')==0 or cleaned_data.get('quantity')=="":
                        continue
                    else:
                        pid = cleaned_data.get('product_id')
                        quantity = cleaned_data.get('quantity')
                        product = Product.objects.get(pk=pid)
                        product_purchase = ProductPurchase()
                        product_purchase.product = product
                        product_purchase.quantity = quantity
                        product_purchase.master_purchase = day_purchase
                        product_purchase.save()
                day_purchase.save()

                return self.form_valid()
        else:
            for form in formset:
                try:
                    form.errors.pop('quantity')
                except KeyError:
                    continue
            form.add_error('quantity', "Quantity field cannot be empty.")
            return self.form_invalid(formset, purchase_form)

    def form_invalid(self, formset, purchase_form):
        return self.render_to_response(self.get_context_data(formset=formset, purchase_form=purchase_form))

    def form_valid(self):
        return HttpResponseRedirect(reverse('purchases:all'))

class DayPurchaseListView(LoginRequiredMixin, ListView):
    model = DayPurchase
    template_name = 'purchases/all_purchases.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        month_sum_dict = {}
        q_set = self.get_queryset()
        context = super(DayPurchaseListView, self).get_context_data(**kwargs)
        purchase_months = q_set.values('month').annotate(g_t=Sum('total')) \
                          .values('month', 'g_t').order_by()

        for p in purchase_months:
            month_sum_dict[calendar.month_name[p.get('month')]] = p.get('g_t')

        context['month_sum_dict'] = month_sum_dict

        return context

class DayPurchaseDetail(LoginRequiredMixin, DetailView):
    template_name = 'purchases/purchase_detail.html'
    model = DayPurchase
    login_url = '/login/'

    payment_form = PaymentForm()

    def get_context_data(self, **kwargs):
        context = super(DayPurchaseDetail, self).get_context_data(**kwargs)
        context['form'] = self.payment_form
        return context

    def post(self, request, *args, **kwargs):
        payment_form = PaymentForm(request.POST)
        self.object = self.get_object()
        if payment_form.is_valid():
            cleaned_data = payment_form.cleaned_data
            payment_option = cleaned_data.get('payment_option')
            if payment_option == '0':
                form_error = check_cheque(payment_form)
                if form_error == True: 
                    print "form error"
                    return self.render_to_response(self.get_context_data(form=payment_form))
                else:
                    cheque = Cheque()
                    cheque.bank = cleaned_data.get('issuing_bank')
                    cheque.account_number = cleaned_data.get('account_number')
                    cheque.cheque_date = cleaned_data.get('cheque_date')
                    cheque.cheque_number = cleaned_data.get('cheque_number')
                    cheque.save()

                    payment = ProductPayment()
                    payment.payment_type = 0 
                    payment.amount_paid = cleaned_data.get('amount_on_cheque')
                    payment.cheque = cheque

                    payment.save()
            else:
                amount_paid = cleaned_data.get('total_cash')
                if amount_paid == None:
                    payment_form.add_error('total_cash', "Please specify the amount paid for the products.")
                    return self.render_to_response(self.get_context_data(form=payment_form))
                else:
                    payment = ProductPayment()
                    payment.payment_type =1 
                    payment.amount_paid = amount_paid
                    payment.save()

            day_purchase = self.get_object()
            day_purchase.payment = payment
            day_purchase.save()
            return HttpResponseRedirect(reverse('purchases:all'))


class PurchaseMetricsView(LoginRequiredMixin, TemplateView):
    template_name = 'purchases/purchase_metrics.html'
    login_url = '/login/'


def check_cheque(form):
    form_error = False
    cleaned_data = form.cleaned_data
    if cleaned_data.get('issuing_bank')=="":
        form.add_error('issuing_bank', "Please provide the name of the bank.")
        form_error = True
    if cleaned_data.get('account_number')=="":
        form.add_error('account_number', "Please provide the account number.")
        form_error = True
    if cleaned_data.get('cheque_number')=="":
        form.add_error('cheque_number', "Please provide the cheque number.")
        form_error = True
    if cleaned_data.get('amount_on_cheque')==None:
        form.add_error('amount_on_cheque', "Please provide the amount on the cheque.")
        form_error = True
    if cleaned_data.get('cheque_date')==None:
        form.add_error('cheque_date', "Please provide the date on cheque.")
        form_error = True
    return form_error
