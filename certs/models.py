from __future__ import unicode_literals

import datetime

from django.db import models

MAX_LENGTH = 1000

"""
TODO: Make MAX_LENGTH changeable through config page
"""


class MetaCertificate(models.Model):
    country_name = models.CharField(max_length=2)
    state_name = models.CharField(max_length=MAX_LENGTH)
    locality_name = models.CharField(max_length=MAX_LENGTH)
    organization_name = models.CharField(max_length=MAX_LENGTH)
    organizational_unit_name = models.CharField(max_length=MAX_LENGTH)
    common_name = models.CharField(max_length=MAX_LENGTH)
    email_address = models.CharField(max_length=MAX_LENGTH)
    certificate = models.TextField()
    signing_request = models.TextField()
    key = models.TextField()
    creation_date = models.DateTimeField()

    @classmethod
    def create_ca_certificate(cls, cert, key, **kwargs):
        """
        TODO: use certificate's creation date but not "now".
        """

        certificate = cls(certificate=cert,
                          key=key,
                          # signing_request=req,
                          creation_date=datetime.datetime.now(),
                          **kwargs)
        certificate.save()
        # do something with the book
        return certificate
    pass

    class Meta:
        abstract = True


class CACertificate(MetaCertificate):
    pass


class Certificate(MetaCertificate):
    pass