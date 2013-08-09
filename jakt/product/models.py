from django.db import models
from utility.models import DatedModel

class Product (DatedModel):
    name = models.CharField(max_length=255)
    related_names = models.CharField(max_length=255, null=True, blank=True, help_text="Comma separated related names")
    image = models.CharField(max_length=255)
    class Meta:
        ordering = ["created"]
    def clean (self, *args, **kwargs):
        super(Product, self).clean(*args, **kwargs)
        self.related_names = ",".join([ s.strip() for s in self.related_names.lower().split(",") ])