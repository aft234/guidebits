from django.db import models
from utility.models import DatedModel

class Product (DatedModel):
    name = models.CharField(max_length=255)
    related_names = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255)
    def clean (self, *args, **kwargs):
        super(self, Product).clean(*args, **kwargs)
        self.related_names = ",".join([ s.trim() for s in self.related_names.lower().split(",") ])