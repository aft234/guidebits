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
        return http.profile(**kwargs)

def merge (token_from, token_to, **kwargs):
    res, status = http.merge(source=token_from, dest=token_to)
    if status != 200:
        logger.error("Failed to merge singly accounts")
    return res