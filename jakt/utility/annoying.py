# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.http import Http404

def set_from_dict (d, *args):
    """Magic happens here."""
    new = {}
    for k in args:
        if d.get(k, None) is not None:
            new[k] = d.get(k)
    globals().update(new)

def difference_lists (a, b):
    """Could be cool."""
    if type(a) is type(b) is list:
        return [ v for v in a if v not in b ]
    return a

def unpack (iterable, level, drop=True):
    """Turns out this is mostly useless"""
    if drop:
        for item in iterable:
            yield tuple(item[0:level])
    else:
        for item in iterable:
            nitem = item[0:level]
            remaining = [ i for i in item[level:]]
            nitem.append(remaining)
            yield tuple(nitem)

def get_or_none (Model, use_objects=None, **kw):
    """Suppress that annoying ObjectDoesNotExist shit."""
    obj = None

    # While you can force this check by specifying ``use_objects`` this
    # is a catch for being lazy.
    if use_objects is None:
        # Do some reflection to figure out if we should use Model.objects.get
        # or just Model.get
        if hasattr(Model, "objects"):
            use_objects = True
        else:
            use_objects = False

    if use_objects:
        get = Model.objects.get
    else:
        get = Model.get

    try:
        obj = get(**kw)
    except ObjectDoesNotExist:
        pass
    except ValueError:
        pass
    return obj

def get_or_raise (*args, **kwargs):
    E = kwargs.pop("exception", LookupError)
    obj = get_or_none(*args, **kwargs)
    if not obj:
        raise E
    return obj

def get_or_gone (*args, **kwargs):
    """Raises Http404 if the object doesn't exist."""
    kwargs["exception"] = Http404
    return get_or_raise(*args, **kwargs)

def default_if_none (obj, default):
    """Allows you to set a default value to something if it is None."""
    if obj is None:
        return default
    return obj

def tree_get (obj, *args):
    """Love this function."""
    val = obj
    for arg in args:
        if val is None:
            return None
        if callable(arg):
            val = arg(val)
        elif isinstance(val, dict):
            val = val.get(arg)
        elif isinstance(val, (list, tuple)):
            try:
                val = val[arg]
            except IndexError:
                return None
        elif isinstance(val, object):
            val = getattr(val, arg, None)
        else:
            # ``val`` is something we can't operate on
            return None
        if val is None:
            return None
    return val