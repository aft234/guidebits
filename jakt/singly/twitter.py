from twython import Twython
from utility.annoying import tree_get
from . import http
from . import twitter_key, twitter_secret

def make_api (*args, **kwargs):
    return Twython(twitter_key, twitter_secret, *args, **kwargs)

def make_api_from_user (user):
    # Do they have singly?
    assert user.singly_token is not None, "{0} does not have a singly token".format(user)

    # Grab the profile
    twitter_profile = http.service_profile("twitter", access_token=user.singly_token, auth="true")
    assert twitter_profile is not None, "No twitter profile returned for {0}".format(user)

    # Grab the key and secret
    keys = tree_get(twitter_profile, "auth", "token")
    assert keys is not None, "No keys returned in the twitter profile for {0}".format(user)
    assert keys.get("oauth_token") is not None
    assert keys.get("oauth_token_secret") is not None
    return make_api(keys.get("oauth_token"), keys.get("oauth_token_secret"))