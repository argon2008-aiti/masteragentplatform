from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from forms import VendorForm
from models import Vendor, ShopAssistant
from sales.models import VendorBooking

from django.db.models import Avg, Sum
import datetime

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = "agent/all_vendors.html"

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        rank_dict = {}
        total_dict = {}
        for index, vendor in enumerate(self.get_queryset()):
            rank_dict[vendor.pk]=index + 1
            total_dict[vendor.pk]=vendor.total

        context['rank'] = rank_dict
        context['total'] = total_dict
        return context

    def get_queryset(self):

        rank = Vendor.objects\
            .annotate(total=Sum('vendorbooking__total'))\
            .order_by('-total')
        try:
            shop_assistant = ShopAssistant.objects.\
                get(user=self.request.user)
            rank = rank.filter(shop=shop_assistant.shop)

        except ShopAssistant.DoesNotExist:
            print "Admin Login"


        return rank

class VendorDetailView(LoginRequiredMixin, DetailView):
    template_name = 'agent/vendor_details.html'
    model = Vendor
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(VendorDetailView, self).get_context_data(**kwargs)
        sales = VendorBooking.objects.filter(vendor=self.object)
        context['sales'] = sales
        print sales
        return context

class VendorJSONListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        from django.core.serializers import serialize
        vendors = Vendor.objects.all()
        return HttpResponse(serialize('json', vendors))


class VendorCreate(LoginRequiredMixin, CreateView):
    form_class = VendorForm
    template_name = "agent/vendor_create_form.html"

    def form_valid(self, form):
        print form
        self.object = form.save()

        if 'shopassistants' in [group.name for group in self.request.user.groups.all()]:
            self.object.agent = self.request.user.shopassistant.shop.agent
            self.object.shop = self.request.user.shopassistant.shop

        elif u'agents' in [group.name for group in self.request.user.groups.all()]:
            self.object.agent = self.request.user.agent

        self.object.save()
        return HttpResponseRedirect(reverse('vendors:all'))

    def form_invalid(self, form):
        print form
        return super(VendorCreate, self).form_invalid(form)

