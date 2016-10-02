import dateutil.parser
import six

from django import forms
from django.core import exceptions
from django.db.models import Max

from .models import CACertificate, Certificate

from OpenSSL import crypto
from certs.certgen.certgen import (
    createKeyPair,
    createCertRequest,
    createCertificate,
)

MAX_LENGTH = 1000
YEARS_MAX = 100

"""
TODO: Make MAX_LENGTH and YEARS_MAX changeable through config page
"""


class CACertificateForm(forms.Form):
    countryName = forms.CharField(label='Country Name (2 letter code) [AU]',
                                  max_length=2,
                                  required=False)
    stateOrProvinceName = forms.CharField(label='State or Province Name (full name) [Some-State]',
                                          max_length=MAX_LENGTH,
                                          required=False)
    localityName = forms.CharField(label='Locality Name (eg, city) []',
                                   max_length=MAX_LENGTH,
                                   required=False)
    organizationName = forms.CharField(label='Organization Name (eg, company) [Internet Widgits Pty Ltd]',
                                       max_length=MAX_LENGTH,
                                       required=False)
    organizationalUnitName = forms.CharField(label='Organizational Unit Name (eg, section) []',
                                             max_length=MAX_LENGTH,
                                             required=False)
    commonName = forms.CharField(label='Common Name (e.g. server FQDN or YOUR name) []',
                                 max_length=MAX_LENGTH,
                                 required=False)
    emailAddress = forms.CharField(label='Email Address []',
                                   max_length=MAX_LENGTH,
                                   required=False)

    @classmethod
    def create_certificate(self, form):
        for key in form.keys():
            temp_str = form[key]
            if isinstance(temp_str, six.string_types):
                form[key] = temp_str.strip()
            if form[key] == '':
                form.pop(key)

        if 'ca_cert' in form.keys():
            # If ca_cert is given, it means that ordinary certificate (not CA certificate)
            # is beeing created.
            # If ca_cert key is in form, then get it and remove from form dict.
            # If ca_key is not removed, then error during createCertRequest will appear
            # because createCertRequest can't handle this key and object.
            ca_cert = form['ca_cert']
            form.pop('ca_cert')

            pkey = createKeyPair(crypto.TYPE_RSA, 2048)
            req = createCertRequest(pkey, **form)

            cakey_x509 = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_cert.key)
            cacert_x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert.cert)

            # Try to get certificate with Max serial.
            # If not found - set serial = 1, because serial = 0 is root CA

            serial_max = Certificate.objects.filter(ca_cert=ca_cert).all().aggregate(Max('serial'))
            if 'serial_max' in serial_max.keys():
                serial = serial_max['serial_max'] + 1
            else:
                serial = 1

            #Create new certificate with serial number equal 'serial + 1'
            cert = createCertificate(req,
                                     (cacert_x509, cakey_x509),
                                     serial,
                                     (0, 60 * 60 * 24 * 365 * YEARS_MAX))

            cert_dump = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
            key_dump = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey).decode('utf-8')
            sign_req_dump = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode('utf-8')
            not_before_date = dateutil.parser.parse(cert.get_notBefore())
            not_after_date = dateutil.parser.parse(cert.get_notAfter())
            Certificate.create_certificate(cert=cert_dump,
                                           key=key_dump,
                                           signingRequest=sign_req_dump,
                                           notBeforeDate=not_before_date,
                                           notAfterDate=not_after_date,
                                           ca_cert=ca_cert,
                                           serial=serial,
                                           **form)
        else:
            # If ca_cert is not given, it means that CA certificate
            # is beeing created.
            cakey = createKeyPair(crypto.TYPE_RSA, 2048)
            careq = createCertRequest(cakey, **form)

            # CA certificate goes with serial = 0
            serial = 0
            cacert = createCertificate(careq,
                                       (careq, cakey),
                                       serial,
                                       (0, 60 * 60 * 24 * 365 * YEARS_MAX))
            cacert_dump = crypto.dump_certificate(crypto.FILETYPE_PEM, cacert).decode('utf-8')
            key_dump = crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey).decode('utf-8')
            sign_req_dump = crypto.dump_certificate_request(crypto.FILETYPE_PEM, careq).decode('utf-8')
            not_before_date = dateutil.parser.parse(cacert.get_notBefore())
            not_after_date = dateutil.parser.parse(cacert.get_notAfter())

            CACertificate.create_certificate(cert=cacert_dump,
                                             key=key_dump,
                                             signingRequest=sign_req_dump,
                                             notBeforeDate=not_before_date,
                                             notAfterDate=not_after_date,
                                             **form)


class CertificateForm(CACertificateForm):
    ca_cert = forms.ModelChoiceField(queryset=CACertificate.objects.all(),
                                     label='Parent CA certificate',
                                     required=True)
