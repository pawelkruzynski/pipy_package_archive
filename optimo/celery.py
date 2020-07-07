from __future__ import absolute_import

import os
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "optimo.settings")

app = Celery("optimo")

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

now = datetime.now() + timedelta(minutes=1)

app.conf.CELERYBEAT_SCHEDULE = {
    "update_packages": {
        "task": "webapps.package.tasks.update_data_from_source",
        "schedule": crontab(minute=now.minute, hour=now.hour),
    },
}
