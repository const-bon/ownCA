from django import forms

from .models import Certificate

from OpenSSL import crypto
from certs.certgen.certgen import (
    createKeyPair,
    createCertRequest,
    createCertificate,
)

MAX_LENGTH = 1000


class CertificateForm(forms.Form):
    country_name = forms.CharField(label='Country Name (2 letter code) [AU]',
                                   max_length=2)
    state_name = forms.CharField(label='State or Province Name (full name) [Some-State]',
                                 max_length=MAX_LENGTH)
    locality_name = forms.CharField(label='Locality Name (eg, city) []',
                                    max_length=MAX_LENGTH)
    organization_name = forms.CharField(label='Organization Name (eg, company) [Internet Widgits Pty Ltd]',
                                        max_length=MAX_LENGTH)
    organizational_unit_name = forms.CharField(label='Organizational Unit Name (eg, section) []',
                                               max_length=MAX_LENGTH)
    common_name = forms.CharField(label='Common Name (e.g. server FQDN or YOUR name) []',
                                  max_length=MAX_LENGTH)
    email_address = forms.CharField(label='Email Address []',
                                    max_length=MAX_LENGTH)

    def create_certificate(self):
        pass

    def create_ca_certificate(self, form):
        # form_data = {'C': str(form['common_name']),
        #              'ST': str(form['state_name']),
        #              'L': str(form['locality_name']),
        #              'O': str(form['organization_name']),
        #              'OU': str(form['organizational_unit_name']),
        #              'CN': str(form['common_name']),
        #              'emailAddress': str(form['email_address'])}
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
        careq = createCertRequest(cakey,
                                  C=str(form['country_name']),
                                  ST=str(form['state_name']),
                                  L=str(form['locality_name']),
                                  O=str(form['organization_name']),
                                  OU=str(form['organizational_unit_name']),
                                  CN=str(form['common_name']),
                                  emailAddress=str(form['email_address']))
        # CA certificate is valid for five years.
        cacert = createCertificate(careq, (careq, cakey), 1, (0, 60 * 60 * 24 * 365 * 5))

        Certificate.create_ca_certificate(form['common_name'],
                                          crypto.dump_certificate(crypto.FILETYPE_PEM, cacert).decode('utf-8'),
                                          crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey).decode('utf-8'))

#
# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)
#
#
# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)
