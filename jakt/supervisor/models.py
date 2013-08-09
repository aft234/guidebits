# coding=utf-8
import logging, uuid
from datetime import date
logger = logging.getLogger(__name__)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.urlresolvers import reverse
from utility import annoying as a

class User (AbstractUser):
    """Extended user model."""

    timezone = models.CharField(max_length=255, default="America/New_York")
    def __unicode__ (self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ["-date_joined"]
        permissions = (
            ( "create_client", "Can create a client" ),
            ( "create_project", "Can create a project" ),
        )