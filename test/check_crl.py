from OpenSSL import crypto

wrong_crl_string = """
-----BEGIN X509 CRL-----
MIIBZjBQMA0GCSqGSIb3DQEBCwUAMAAYDzIwMTYxMTI5MTk0NzAyWjAsMBQCAQAY
DzIwMTYxMTI5MTk0NzAyWjAUAgEBGA8yMDE2MTEyOTE5NDcwMlowDQYJKoZIhvcN
AQELBQADggEBAEnxcWxuqNtc2AfXKrZSOZ2lGY24R9J8Uh2hZwjJd0qqsNkPcJW3
bJ61U0UC1YaLY/j9vPtiSkIKLxFTM/UYWZ4bXptvcSssJtNnZB/C5Y7uW+DpPpRb
094YSf5gcOetrhaHqUY/3fs+s8C4Vuby8Xv6uT6TCi0bJxMO1sVHze7026z9JDZo
uxu9ztxDas6IBdmhQ0j+CuPew2aO8voV7QrNkK1D4EHJRX92vdbxrw25ASkd4MFW
iMjI3n2/be2eujFhq74uuB29YXGuI54MKIxikb5iv/1D8Imxk4pGpaCqQxxpoHXy
A/RpKhe98wH+TptfPy5NEV7fhrPY+D63gl0=
-----END X509 CRL-----
"""

correct_crl_string = """
-----BEGIN X509 CRL-----
MIIBtDCBnQIBATANBgkqhkiG9w0BAQsFADBFMQswCQYDVQQGEwJBVTETMBEGA1UE
CAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRk
Fw0xNjExMjkxODQ0MzNaFw0xNjEyMjkxODQ0MzNaMBQwEgIBARcNMTYxMDAyMTgy
NjIxWqAOMAwwCgYDVR0UBAMCAQQwDQYJKoZIhvcNAQELBQADggEBACPz2sCIa9oR
jDHqOF42BIj2wEKCTKOCPT8KdpA2onQrrpn0y/quRiJ7xPNX53y6XoVq0Kr51hCu
qqVDz/bGQHZu1ATW5k5nUF0NbWeGCXqDj8eFMZG5WoUgVwyR1pez4YtqTgyxmTZI
EhAWHaBCqZ9Sm6Oh9acuSd06pTH8ZD5N4heCx0prOmZXmgSNRLd/qZtdAOAcO0aw
NAyTlXAkjvb4TM/Yx9eAgS5/rqU6NjlCmdWb2xvFzh8zRv5fnWAOBLvaW2dOuWkQ
XbMJ20v1nOd4W6+Wi/oe0XwxLSp7I6tuFqinhZ3xorrDdVfObh+tCgABQlxPx7OO
JzFySUnZWHk=
-----END X509 CRL-----
"""

correct_crl = crypto.load_crl(crypto.FILETYPE_PEM, correct_crl_string)
revoked_list = correct_crl.get_revoked()
for revoked in revoked_list:
    print(revoked.get_serial())
    print(revoked.get_rev_date())

wrong_crl = crypto.load_crl(crypto.FILETYPE_PEM, wrong_crl_string)
revoked_list = wrong_crl.get_revoked()
for revoked in revoked_list:
    print(revoked.get_serial())
    print(revoked.get_rev_date())
