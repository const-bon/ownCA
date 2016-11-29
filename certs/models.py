from __future__ import unicode_literals

import time

from django.db import models

from OpenSSL import crypto

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
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.pk, self.commonName)

    @classmethod
    def create_certificate(cls, **kwargs):
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
    serial = models.IntegerField()
    """
    TODO:
    Make serial be different certificates
    """
    """
    TODO:
    Use serial based on epoch for CA certificate
    """
    def revoke(self):
        self.revoked = True
        self.save()

    @staticmethod
    def get_crl(ca_cert, digest=b"sha256"):
        # Search revoked certificates with CA certificate 'ca_cert' in table Certificate
        cert_list = Certificate.objects.filter(ca_cert=ca_cert, revoked=True)
        if cert_list:
            crl = crypto.CRL()
            for cert in cert_list:
                revoked = crypto.Revoked()
                serial_hex = hex(cert.serial)
                serial_hex = serial_hex[2:]
                revoked.set_serial(serial_hex)
                current_time = time.strftime('%Y%m%d%H%M%SZ', time.gmtime(time.time()))
                revoked.set_rev_date(current_time)
                crl.add_revoked(revoked)
            cakey_x509 = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_cert.key)
            cacert_x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert.cert)
            crl.set_lastUpdate(current_time)
            crl.sign(cacert_x509, cakey_x509, digest)
            return crypto.dump_crl(crypto.FILETYPE_PEM, crl).decode('utf-8')
        else:
            return None
