import logging
logger = logging.getLogger(__name__)
import json
from django.db import models
from utility.models import DatedModel
from utility.annoying import tree_get
from . import words
class Product (DatedModel):
    name = models.CharField(max_length=255)
    related_names = models.CharField(max_length=255, null=True, blank=True, help_text="Comma separated search terms to use in OR")
    image = models.CharField(max_length=255)
    class Meta:
        ordering = ["created"]
    def clean (self, *args, **kwargs):
        super(Product, self).clean(*args, **kwargs)
        self.related_names = ",".join([ s.strip() for s in self.related_names.lower().split(",") ])

    @property
    def related_names_list (self):
        return [ s.strip() for s in self.related_names.lower().split(",") ]

class Search (DatedModel):
    product = models.ForeignKey(Product)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    total_results = models.IntegerField(default=0)
    blob_results = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created"]

    def set_status (self, s):
        self.status = s
        self.save()

    def set_results (self, blob):
        self.blob_results = json.dumps(blob)

    def get_results (self):
        return json.loads(self.blob_results)

    def _total_for_category (self, c):
        results = self.get_results()
        return tree_get(results, c, "num")

    @property
    def descriptions (self):
        return self._total_for_category("descriptor")
    @property
    def emotions (self):
        return self._total_for_category("emotion")
    @property
    def possessives (self):
        return self._total_for_category("possessive")
    @property
    def promotionals (self):
        return self._total_for_category("promotional")
    @property
    def reactions (self):
        return self._total_for_category("reaction")
    @property
    def intents (self):
        return self._total_for_category("intent")

    @property
    def all_word_pairs (self):
        results = self.get_results()
        for d in results.values():
            listed_words = d["words"]
            items = map(lambda (w, l): l, listed_words.iteritems())
            if not items:
                continue
            low = min(items)
            high = max(items)
            zero = max(float(high - low) * 10, high)
            for w, l in listed_words.iteritems():
                percent = float(l) / zero
                yield (w, words.reverse(w), l, percent)

class Tweet (DatedModel):
    search = models.ForeignKey(Search)
    text = models.TextField(null=True, blank=True)

class Word (models.Model):
    CATEGORIES = (
        ("emotion", "Emotion"),
        ("description", "Description"),
        ("intent", "Intent"),
        ("possessive", "Possessive"),
        ("reaction", "Reaction"),
    )
    parent = models.CharField(max_length=255, choices=CATEGORIES)
    root = models.CharField(max_length=255)
    synonyms = models.TextField()