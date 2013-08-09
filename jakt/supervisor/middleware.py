import pytz
from django.utils import timezone
from django.conf import settings

class TimezoneMiddleware (object):
    """Configures the timezone from the session if available. Attempts
    to set the timezone if it's missing using `TIME_ZONE` from settings
    or the user's timezone if available."""
    def process_request(self, request):
        if not request.session.get("timezone"):
            request.session["timezone"] = settings.TIME_ZONE
            if request.user.is_authenticated() and request.user.timezone:
                request.session["timezone"] = request.user.timezone
        timezone.activate(pytz.timezone(request.session.get("timezone")))
