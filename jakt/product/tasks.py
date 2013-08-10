# coding=utf-8
"""Celery tasks"""

import logging
logger = logging.getLogger(__name__)

from celery import task

@task
def speak ():
    logger.critical('Speaking!')