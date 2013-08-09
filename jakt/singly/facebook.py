# coding=utf-8

# General imports
import logging
logger = logging.getLogger(__name__)

# Project imports
from utility import annoying as a

# Internal imports
from singly import http

def get_profile (access_token, **kwargs):
    if access_token is None:
        logger.error("Unable to fetch profile without an access_token")
    else:
        kwargs["access_token"] = access_token
        return http.service_profile("facebook", **kwargs)

def get_friends (access_token, **kwargs):
    logger.debug("Fetching friends")
    if access_token is None:
        logger.error("Unable to fetch friends without an access_token")
    else:
        with http.get("https://api.singly.com/proxy/facebook/me/friends", params={"access_token":access_token}) as r:
            return [ a.tree_get(p, "id") for p in a.tree_get(r.json(), "data") ]

def get_mutual_friends (access_token, other_id=None, **kwargs):
    logger.debug("Fetching mutual friends")
    if access_token is None:
        logger.error("Unable to fetch mutual friends without an access_token")
    else:
        url = "https://api.singly.com/proxy/facebook/me/mutualfriends/{other_id}".format(other_id=other_id)
        kwargs["access_token"] = access_token
        with http.get(url, params=kwargs) as r:
            return a.tree_get(r.json(), "data")