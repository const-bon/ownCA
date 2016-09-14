from __future__ import unicode_literals

import datetime

from django.db import models

MAX_LENGTH = 1000

"""
TODO: Make MAX_LENGTH changeable through config page
"""


class MetaCertificate(models.Model):
    countryName = models.CharField(max_length=2)
    stateOrProvinceName = models.CharField(max_length=MAX_LENGTH)
    localityName = models.CharField(max_length=MAX_LENGTH)
    organizationName = models.CharField(max_length=MAX_LENGTH)
    organizationalUnitName = models.CharField(max_length=MAX_LENGTH)
    commonName = models.CharField(max_length=MAX_LENGTH)
    emailAddress = models.CharField(max_length=MAX_LENGTH)
    cert = models.TextField()
    signingRequest = models.TextField()
    key = models.TextField()
    notBeforeDate = models.DateTimeField()
    notAfterDate = models.DateTimeField()

    @classmethod
    def create_certificate(cls, **kwargs):
        """
        TODO: use certificate's creation date but not "now".
        """

        cert = cls(**kwargs)
        cert.save()
        # do something with the book
        return cert

    class Meta:
        abstract = True


class CACertificate(MetaCertificate):
    pass


class Certificate(MetaCertificate):
    ca_cert = models.ForeignKey(CACertificate)
