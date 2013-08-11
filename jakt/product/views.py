# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from utility.annoying import get_or_gone as gog
from .models import Product, Search
from .forms import ProductForm
from . import tasks
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

def searches (request, pk):
    data = {}
    data["product"] = product = gog(Product, pk=pk)
    data["searches"] = product.search_set.all()
    return render(request, "product/searches.html", data)

def add_search (request, pk):
    product = gog(Product, pk=pk)
    search = Search(product=product, status="Queued")
    search.save()
    tasks.perform_search.delay(search.pk)
    return HttpResponseRedirect(reverse("product.views.searches", kwargs={"pk" : product.pk}))