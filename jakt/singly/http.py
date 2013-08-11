# coding=utf-8
import logging, requests
logger = logging.getLogger(__name__)

from singly import client_id, client_secret, api_url

SERVICE_SCOPES = {
    "facebook" : "email,offline_access",
    "linkedin" : "r_emailaddress r_fullprofile"
}

BASE_URL = api_url

class MethodManager (object):
    """Base Context Manager the handles repetative arguments and logging."""

    def __init__ (self, method, url, *args, **kwargs):
        """Initializes the method, url, and positional / keyword arguments for any request method."""
        self.method = method
        self.url = url
        self.args = args
        self.session = None
        if "session" in kwargs:
            self.session = kwargs.get("session")
            del kwargs["session"]
        self.kwargs = kwargs

    def __enter__ (self):
        """Handles a request start."""
        logger.debug(u"{method} fetching {url} with {args} and {kwargs}".format(method=self.method.upper(), url=self.url, args=self.args, kwargs=self.kwargs))
        try:
            assert self.url is not None
            self.r = getattr(self.reqs, self.method)(self.url, *self.args, **self.kwargs)
        except:
            if not self.__exit__(*sys.exc_info()):
                raise
        else:
            if isinstance(getattr(self, "r", None), requests.models.Response):
                return self.r

    def __exit__ (self, ext_type, value, traceback):
        """Handles a request exit and exception checking."""
        if isinstance(getattr(self, "r", None), requests.models.Response):
            logger.debug(u"Exiting {method} with {status} for {url}".format(method=self.method.upper(), status=self.r.status_code, url=self.r.url))
        else:
            logger.error(u"Exiting {method} with no response object".format(method=self.method.upper()))
            logger.error(u"{0} {1} {2}".format(ext_type, value, traceback))
        if value and issubclass(ext_type, BaseException):
            logger.exception(value)
            logger.error(traceback)
            logger.warn(u"Exit {method} threw an exception".format(method=self.method.upper()))
        elif value:
            logger.fatal(u"Something wonky happened.")
            logger.fatal(u"type={type} value={value} traceback={traceback}".format(type=ext_type, value=value, traceback=traceback))
            logger.fatal(u"Exit {method} was definitely dirty".format(method=self.method.upper()))
        elif not isinstance(getattr(self, "r", None), requests.models.Response):
            logger.fatal(u"No response object was returned.")
        elif self.r.status_code not in [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]:
            logger.fatal(u"Response was not 2XX: {response}".format(response=self.r))
            logger.fatal(u"Path: {url}".format(url=self.r.url))
            logger.fatal(u"Response: {text}".format(text=self.r.text))
        else:
            logger.debug(u"Exit {method} was clean".format(method=self.method.upper()))
        return True

    @property
    def reqs (self):
        if self.session:
            return self.session
        return requests

def bind_verb (verb):
    class _verb (MethodManager):
        def __init__ (self, url, *args, **kwargs):
            super(_verb, self).__init__(verb, url, *args, **kwargs)
    return _verb

get = bind_verb("get")
post = bind_verb("post")
delete = bind_verb("delete")

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