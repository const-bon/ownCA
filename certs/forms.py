from django import forms

from .models import CACertificate

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


class CertificateForm(forms.Form):
    country_name = forms.CharField(label='Country Name (2 letter code) [AU]',
                                   max_length=2,
                                   required=False)
    state_name = forms.CharField(label='State or Province Name (full name) [Some-State]',
                                 max_length=MAX_LENGTH,
                                 required=False)
    locality_name = forms.CharField(label='Locality Name (eg, city) []',
                                    max_length=MAX_LENGTH,
                                    required=False)
    organization_name = forms.CharField(label='Organization Name (eg, company) [Internet Widgits Pty Ltd]',
                                        max_length=MAX_LENGTH,
                                        required=False)
    organizational_unit_name = forms.CharField(label='Organizational Unit Name (eg, section) []',
                                               max_length=MAX_LENGTH,
                                               required=False)
    common_name = forms.CharField(label='Common Name (e.g. server FQDN or YOUR name) []',
                                  max_length=MAX_LENGTH,
                                  required=False)
    email_address = forms.CharField(label='Email Address []',
                                    max_length=MAX_LENGTH,
                                    required=False)

    def create_certificate(self):
        pass

    def create_ca_certificate(self, form):
        form_data = {}
        for key in form:
            if form[key] != '':
                form_data[key] = str(form[key])

        cakey = createKeyPair(crypto.TYPE_RSA, 2048)
        """
        Create a certificate request.

        Arguments: pkey   - The key to associate with the request
                   digest - Digestion method to use for signing, default is sha256
                   **name - The name of the subject of the request, possible
                            arguments are:
                              C     - Country name
                              ST    - State or province name
                              L     - Locality name (eg, city)
                              O     - Organization name
                              OU    - Organizational unit name
                              CN    - Common name
                              emailAddress - E-mail address
        """
        if len(form_data) == 0:
            careq = createCertRequest(cakey)
        else:
            careq = createCertRequest(cakey, **form_data)
        # CA certificate is valid for five years.
        cacert = createCertificate(careq, (careq, cakey), 1, (0, 60 * 60 * 24 * 365 * YEARS_MAX))
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cacert).decode('utf-8')
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey).decode('utf-8')

        CACertificate.create_ca_certificate(cert, key, **form_data)


