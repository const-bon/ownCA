from __future__ import unicode_literals

import datetime

from django.db import models


class Certificate(models.Model):
    common_name = models.CharField(max_length=1024)
    certificate = models.TextField()
    signing_request = models.TextField()
    key = models.TextField()
    creation_date = models.DateTimeField()

    @classmethod
    def create_ca_certificate(cls, common_name, certificate, key):
        """
        TODO: use certificate's creation date but not "now".
        """
        certificate = cls(common_name=common_name,
                          certificate=certificate,
                          key=key,
                          creation_date=datetime.datetime.now())
        certificate.save()
        # do something with the book
        return certificate
