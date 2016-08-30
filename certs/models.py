from __future__ import unicode_literals

from django.db import models


class Certificate(models.Model):
    common_name = models.CharField(max_length=1024)
    certificate = models.TextField()
    signing_request = models.TextField()
    key = models.TextField()
    creation_date = models.DateTimeField()
