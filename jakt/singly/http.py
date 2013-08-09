# coding=utf-8
import logging, requests
logger = logging.getLogger(__name__)

from singly import client_id, client_secret

SERVICE_SCOPES = {
    "facebook" : "email,offline_access",
    "linkedin" : "r_emailaddress r_fullprofile"
}

BASE_URL = "https://api.singly.com"

class MethodManager (object):
    """Base Context Manager the handles repetative arguments and logging."""

    def __init__ (self, method, url, *args, **kwargs):
        """Initializes the method, url, and positional / keyword arguments for any request method."""
        self.method = method
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def __enter__ (self):
        """Handles a request start."""
        logger.debug("{method} fetching {url} with {args} and {kwargs}".format(method=self.method.upper(), url=self.url, args=self.args, kwargs=self.kwargs))

    def __exit__ (self, ext_type, value, traceback):
        """Handles a request exit and exception checking."""
        logger.debug("Exiting {method} with {status} for {url}".format(method=self.method.upper(), status=self.r.status_code, url=self.r.url))
        if value and issubclass(ext_type, BaseException):
            logger.exception(value)
            logger.error(traceback)
            logger.warn("Exit {method} threw an exception".format(method=self.method.upper()))
        elif value:
            logger.fatal("Something wonky happened.")
            logger.fatal("type={type} value={value} traceback={traceback}".format(type=ext_type, value=value, traceback=traceback))
            logger.fatal("Exit {method} was definitely dirty".format(method=self.method.upper()))
        elif self.r.status_code != 200:
            logger.fatal("Response was not 200 OK: {response}".format(response=self.r))
            logger.fatal("Path: {url}".format(url=self.r.url))
            logger.fatal("Response: {text}".format(text=self.r.text))
        else:
            logger.debug("Exit {method} was clean".format(method=self.method.upper()))
        return True

class get (MethodManager):
    """Subclass of MethodManager that handles GET requests."""
    def __init__ (self, url, *args, **kwargs):
        """Initializes the GET request."""
        super(get, self).__init__("get", url, *args, **kwargs)

    def __enter__ (self):
        """Starts the GET request."""
        super(get, self).__enter__()
        self.r = requests.get(self.url, *self.args, **self.kwargs)
        return self.r

class post (MethodManager):
    """Subclass of MethodManager that handles POST requests."""
    def __init__ (self, url, *args, **kwargs):
        """Initializes the POST request."""
        super(post, self).__init__("post", url, *args, **kwargs)

    def __enter__ (self):
        """Starts the POST request."""
        super(post, self).__enter__()
        self.r = requests.post(self.url, *self.args, **self.kwargs)
        return self.r


def create_url (path, **kwargs):
    url = "{base}{path}".format(base=BASE_URL, path=path)
    if kwargs:
        query = "&".join([ "{0}={1}".format(k, v) for k, v in kwargs.items() ])
        url += "?{query}".format(query=query)
    logger.debug("Created url {0}".format(url))
    return url

def connect (service, **kwargs):
    kwargs["client_id"] = client_id
    kwargs["service"] = service
    if SERVICE_SCOPES.get(service):
        kwargs["scope"] = SERVICE_SCOPES.get(service)
    return create_url("/oauth/authenticate", **kwargs)

def service_profile (service, **kwargs):
    with get(create_url("/profiles/{0}".format(service)), params=kwargs) as r:
        return r.json()

def profile (**kwargs):
    with get(create_url("/profile"), params=kwargs) as r:
        return r.json()

def merge (source=None, dest=None, **kwargs):
    with get(create_url("/auth/merge", source=source, dest=dest), params=kwargs) as r:
        return r.json(), r.status_code

def fetch_token (code, **kwargs):
    kwargs["client_id"] = client_id
    kwargs["client_secret"] = client_secret
    kwargs["code"] = code
    url = create_url("/oauth/access_token")
    with post(url, data=kwargs) as r:
        return r.json()