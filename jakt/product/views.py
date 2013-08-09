# coding=utf-8

from django.shortcuts import render
from .models import Product
def all (request):
    data = {}
    data["products"] = Product.objects.all()
    return render(request, "product/all.html", data)
