# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from utility.annoying import get_or_gone as gog
from supervisor.decorators import requires_staff
from .models import Product, Search, Tweet
from .forms import ProductForm
from . import tasks

def all (request):
    data = { "products" : [] }
    data["products"] = Product.objects.filter(active=True)
    data["latest_tweets"] = Tweet.objects.filter(valid=True)[:30]
    return render(request, "product/all.html", data)

@requires_staff
def management (request):
    data = {}
    data["products"] = Product.objects.all()
    data["active_searches"] = Search.objects.filter(complete=False)
    return render(request, "product/management.html", data)

@requires_staff
def add (request):
    data = {}
    form = ProductForm()
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect(reverse("product.views.add_search", kwargs={"pk" : product.pk}))
    data["form"] = form
    return render(request, "product/add.html", data)

@requires_staff
def edit (request, pk):
    data = {}
    data["product"] = product = gog(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.POST:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("product.views.view_product", kwargs={"pk" : product.pk}))
    data["form"] = form
    return render(request, "product/edit.html", data)

def view_product (request, pk):
    import time
    data = {}
    offset = int(request.GET.get("offset", 0))
    if offset != 0:
        time.sleep(5)
    data["product"] = gog(Product, pk=pk)
    data["is_staff"] = request.user.is_staff
    if not request.user.is_staff:
        data["product"] = gog(Product, pk=pk, active=True)

    data["last_tweets"] = Tweet.objects.filter(product=data["product"], valid=True).order_by("-created_at")[offset:offset+30]
    data["offset"] = offset + 30
    return render(request, "product/view_product.html", data)

@requires_staff
def view_tweets (request, pk):
    data = {}
    data["product"] = product = gog(Product, pk=pk)
    data["tweets"] = product.tweet_set.filter(valid=True).order_by("-created_at")
    return render(request, "product/view_tweets.html", data)

@requires_staff
def searches (request, pk):
    data = {}
    data["product"] = product = gog(Product, pk=pk)
    data["searches"] = product.search_set.all()
    data["word_pairs"] = product.all_word_pairs
    return render(request, "product/searches.html", data)

@requires_staff
def view_search (request, pk):
    data = {}
    data["search"] = search = gog(Search, pk=pk)
    data["product"] = search.product
    return render(request, "product/view_search.html", data)

@requires_staff
def delete_search (request, pk):
    data = {}
    search = gog(Search, pk=pk)
    product = search.product
    if request.POST and request.POST.get("confirm") == search.product.name:
        search.delete()
        product.update_search_cache()
    return HttpResponseRedirect(reverse("product.views.management"))

@requires_staff
def add_search (request, pk):
    product = gog(Product, pk=pk)
    search = Search(product=product, status="Queued")
    search.save()
    tasks.perform_search.delay(search.pk)
    return HttpResponseRedirect(reverse("product.views.searches", kwargs={"pk" : product.pk}))