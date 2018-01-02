import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import FormMixin, ModelFormMixin, FormView

from public.forms import ServiceCreationForm, ReviewCreationForm
from public.models import Product, ServiceProvider, Review


def home(request):
    return render(request, 'home.html', {})

class ProductListView(ListView):
    model = ServiceProvider
    context_object_name = 'products'
    template_name = 'product_list.html'

class ServiceDetail(DetailView):
    """ The page that shows the service provider main page( all his info, rating, reviews, and products """
    model = ServiceProvider
    template_name = 'service_detail.html'
    context_object_name = 'service'

    def get_context_data(self,*args ,**kwargs):
        context=super().get_context_data()
    #    context['products']=Product.objects.filter(created_by=self.kwargs['pk'])
        context['reviews'] = Review.objects.filter(review_of=self.kwargs['pk'])
        context['form'] = ReviewCreationForm
        return context

class ServiceCreation(CreateView):
    """ The view to create a new Service """
    form_class = ServiceCreationForm
    template_name = 'service_creation.html'
    #success_url = reverse_lazy('public:service_detail', kwargs={'pk':self.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ServiceCreation, self).form_valid(form)

class ServiceUpdate(UpdateView):
    """ The view to modify service's info """
    model = ServiceProvider
    fields = ['name',  'description', 'photo', 'location', 'website']
    template_name = 'service_creation.html'

class ProductCreation(CreateView):
    model = Product
    fields = ['name','description', 'photo', 'price']
    template_name = 'product_creation.html'


    def form_valid(self, form):
        service = ServiceProvider.objects.filter(creator=self.request.user).first()
        form.instance.created_by = service
        return super(ProductCreation, self).form_valid(form)

class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['reviews']=Review.objects.filter(product__pk=self.kwargs['pk'])
        context['form'] = ReviewCreationForm
        return context




class ReviewCreation(FormView):


    form_class = ReviewCreationForm
    success_url = 'home'

    def  post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        service = ServiceProvider.objects.filter(creator=self.request.user).first()
        form.instance.created_by = self.request.user
    #    form.instance.review_of=service
    #    form.instance.product=Product.objects.get(created_by=service)
        return super(ReviewCreation, self).form_valid(form)


def product_review_form(request):
    """ The Form handling for Product Detail view"""
    if request.method=='POST':
        service = ServiceProvider.objects.filter(creator=request.user).first()
        product = Product.objects.get(created_by=service)
        form=ReviewCreationForm(request.POST)
        form.instance.created_by = request.user
# This is for service provider reviews it self not product so no need for it
#        form.instance.review_of=service
        form.instance.product= product
        form.save()
        return redirect('public:product_detail', product.pk)
    form=ReviewCreationForm()
    return render(request, 'product_detail.html', {'form':form})

def service_review_form(request):
    """ The Form handling for Service Detail view"""
    if request.method == 'POST':
        service = ServiceProvider.objects.filter(creator=request.user).first()
        form = ReviewCreationForm(request.POST)
        form.instance.created_by = request.user

        form.instance.review_of=service
#      this is for product not service so no need for it
#        form.instance.product = Product.objects.get(created_by=service)
        form.save()
        return redirect('public:service_detail', service.pk)
    form = ReviewCreationForm()
    return render(request, 'service_detail.html', {'form': form})