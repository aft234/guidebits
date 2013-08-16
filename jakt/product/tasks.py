# coding=utf-8
"""Celery tasks"""

import logging
import json
logger = logging.getLogger(__name__)
from singly import twitter
from celery import task

from utility.annoying import get_or_raise as gor, tree_get
from supervisor.models import User
from .models import Product, Search, Tweet
from . import words

@task
def speak ():
    logger.critical('Speaking!')

@task
def perform_search (pk):
    search = gor(Search, pk=pk)
    product = search.product
    logger.info("Starting search for {0}".format(product.name))

    # Do a standard twitter search for the product OR any associated names
    query = " OR ".join(product.related_names_list)
    count = 100

    logger.info("Query is {0}".format(query))
    search.set_status("Finding user for Twitter search")
    # Now find an applicable twitter user, prefer one with >10 search limits available
    possibles = User.objects.exclude(singly_token=None)
    user = None
    api = None
    for user in possibles:
        # Construct a new twitter api object and check the remaining calls for /search/tweets
        api = twitter.make_api_from_user(user)
        limits = api.get_application_rate_limit_status()
        search_remaining = tree_get(limits, "resources", "search", "/search/tweets", "remaining")
        if search_remaining >= 15:
            break
        user = None

    if user is None:
        search.set_status("Failed. No twitter requests remaining.")
        return

    # Iterate over the search results appending new statuses as they are found
    search.set_status("Collecting results from twitter")
    statuses = []
    results = api.search(q=query, count=count, lang='en')
    while len(results.get("statuses")) == count:
        statuses.extend(results.get("statuses"))
        results = api.search(q=query, count=count, lang='en', max_id=statuses[-1].get("id_str"))

    # Now generate a results map for these statuses
    num_statuses = len(statuses)
    logger.info("Found {0} statuses".format(num_statuses))
    search.total_results = num_statuses
    search.save()
    result_dict = { c : { "num" : 0, "words" : {} } for c in words.categories }
    for i, status in enumerate(statuses):
        search.set_status("Processing status {0} of {1}".format(i + 1, num_statuses))
        tweet = Tweet.create(search, status)
        status_text = status.get("text").lower().strip()
        if status_text[0:9] == "i liked a" or status_text[0:13] == "i favorited a" or status_text[0:14] == "i favourited a" or status_text[0:9] == "i added a":
            continue
        if status_text[0:14] == "i'm now ranked":
            continue
        if status.get("retweeted_status"):
            continue
        word_set = set(status_text.split(" "))

        # For every word category we have defined
        for c in words.categories:
            c_list = []

            # Grab all the matching words from the tweet
            c_words = word_set & getattr(words, "{0}_set".format(c))
            if not c_words:
                continue
            tweet.valid = True
            # Sanitize / reverse those words
            for w in c_words:
                c_list.append(getattr(words, c)[w])

            # Unique them with a set and increase the total for that category
            c_list = set(c_list)
            result_dict[c]["num"] += len(c_list)
            for w in c_list:
                result_dict[c]["words"].setdefault(w, 0)
                result_dict[c]["words"][w] += 1
        tweet.save()
    search.blob_results = json.dumps(result_dict)
    search.complete = True
    search.set_status("Complete")
    search.save()
    product.update_search_cache()
    logger.info("Done performing search")