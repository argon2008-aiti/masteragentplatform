from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, View
from forms import VendorForm
from models import Vendor

class VendorListView(LoginRequiredMixin, TemplateView):
    template_name = "agent/all_vendors.html"


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

        elif u'agents' in [group.name for group in self.request.user.groups.all()]:
            self.object.agent = self.request.user.agent

        self.object.save()
        return HttpResponseRedirect(reverse('vendors:all'))
    
    def form_invalid(self, form):
        print form
        return super(VendorCreate, self).form_invalid(form)

