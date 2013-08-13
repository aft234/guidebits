# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from utility.annoying import get_or_gone as gog
from .models import Product, Search
from .forms import ProductForm
from . import tasks

def all (request):
    data = { "products" : [] }
    products = Product.objects.all()
    for product in products:
        last_search = None
        if product.search_set.count():
            last_search = product.search_set.all()[0]
        data["products"].append((product, last_search))
    return render(request, "product/all.html", data)

def management (request):
    data = {}
    data["products"] = Product.objects.all()
    data["active_searches"] = Search.objects.filter(complete=False)
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

def view_search (request, pk):
    data = {}
    data["search"] = gog(Search, pk=pk)
    return render(request, "product/view_search.html", data)

def delete_search (request, pk):
    data = {}
    search = gog(Search, pk=pk)
    if request.POST and request.POST.get("confirm") == search.product.name:
        search.delete()
    return HttpResponseRedirect(reverse("product.views.management"))

def add_search (request, pk):
    product = gog(Product, pk=pk)
    search = Search(product=product, status="Queued")
    search.save()
    tasks.perform_search.delay(search.pk)
    return HttpResponseRedirect(reverse("product.views.searches", kwargs={"pk" : product.pk}))