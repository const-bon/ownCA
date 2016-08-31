#!/bin/bash

#CA
function ca {
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -key rootCA.key -days 36500 -out rootCA.crt
}

#custom key
function custom {
openssl genrsa -out server102.mycloud.key 2048
openssl req -new -key server102.mycloud.key -out server102.mycloud.csr
openssl x509 -req -in server102.mycloud.csr \
                -CA rootCA.crt -CAkey rootCA.key \
                -CAcreateserial -out server102.mycloud.crt -days 5000
}

custom