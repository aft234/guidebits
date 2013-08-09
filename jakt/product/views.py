# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from utility.annoying import get_or_gone as gog
from .models import Product
from .forms import ProductForm

def all (request):
    data = {}
    data["products"] = Product.objects.all()
    return render(request, "product/all.html", data)

def management (request):
    data = {}
    data["products"] = Product.objects.all()
    return render(request, "product/management.html", data)

def add (request):
    data = {}
    form = ProductForm()
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("product.views.management"))
    data["form"] = form
    return render(request, "product/add.html", data)

def edit (request, pk):
    data = {}
    product = gog(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.POST:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("product.views.management"))
    data["form"] = form
    return render(request, "product/edit.html", data)