import logging
import math
import json
from dateutil.parser import parse as parse_date
from django.db import models
from utility.models import DatedModel
from utility.annoying import tree_get
from . import words

logger = logging.getLogger(__name__)

class Product (DatedModel):
    name = models.CharField(max_length=255)
    related_names = models.CharField(max_length=255, null=True, blank=True, help_text="Comma separated search terms to use in OR")
    image = models.CharField(max_length=255, null=True, blank=True, help_text="Link to image of product")
    search_cache = models.TextField(null=True, blank=True)
    buy_link = models.CharField(max_length=255, null=True, blank=True, help_text="Referral or direct link to purchase this product")
    description = models.TextField(null=True, blank=True, help_text="HTML Description for the product")

    class Meta:
        ordering = ["created"]
    def clean (self, *args, **kwargs):
        super(Product, self).clean(*args, **kwargs)
        self.related_names = ",".join([ s.strip() for s in self.related_names.lower().split(",") ])

    @property
    def related_names_list (self):
        return [ s.strip() for s in self.related_names.lower().split(",") ]

    def set_search_cache (self, blob):
        self.search_cache = json.dumps(blob)
        self.save()
    def get_search_cache (self):
        return json.loads(self.search_cache)

    def update_search_cache (self):
        categories = { k : { "total" : 0, "words" : {} } for k in words.categories }

        for search in self.search_set.all():
            results = search.get_results()
            for category, result_map in results.iteritems():
                categories[category]["total"] += result_map.get("num", 0)
                for w, l in result_map["words"].iteritems():
                    categories[category]["words"].setdefault(w, 0)
                    categories[category]["words"][w] += l
        self.set_search_cache(categories)

    @property
    def all_word_pairs (self):
        results = self.get_search_cache()
        for c, d in results.iteritems():
            listed_words = d["words"]
            items = map(lambda (w, l): l, listed_words.iteritems())
            if not items:
                continue
            words = sorted(listed_words.iteritems(), key=lambda w: w[1])
            for w, l in words[:25]:
                yield (w, c, l, math.log(l))
            # for w, l in listed_words.iteritems():
                # percent = float(l) / zero
                # yield (w, c, l, l)
                # pass

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
            if not listed_words:
                continue
            for w, l in listed_words.iteritems():
                yield (w, words.reverse(w), l, math.log(l))

class Tweet (DatedModel):
    search = models.ForeignKey(Search)
    product = models.ForeignKey(Product)
    valid = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    tweet_id = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField()
    raw = models.TextField()

    @staticmethod
    def create (search, status):
        tw = Tweet(search=search, product=search.product)
        tw.text = tree_get(status, "text")
        tw.user_id = tree_get(status, "user", "id_str")
        tw.name = tree_get(status, "user", "name")
        tw.screen_name = tree_get(status, "user", "screen_name")
        tw.tweet_id = tree_get(status, "id_str")
        tw.created_at = parse_date(tree_get(status, "created_at"))
        tw.raw = json.dumps(status)
        tw.save()
        return tw

    def display_as_embed (self):
        return u'<blockquote class="twitter-tweet"><p>{t.text}</p>&mdash;{t.name} (@{t.screen_name}) <a href="https://twitter.com/{t.screen_name}/status/{t.tweet_id}" data-datetime="{date}">{nice_date}</a></blockquote>'.format(t=self, date=self.created_at.isoformat(), nice_date=self.created_at.strftime("%B %d, %Y"))

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