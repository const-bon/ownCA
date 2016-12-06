# Docker
https://hub.docker.com/r/comeanother/ownca/

sudo docker run -d -P comeanother/ownca:latest

# Purpose
ownCA is a project aimed at providing users with the possibility of creating and managing their own Public Key Infrastructure (PKI) using the built-in web interface. 

## Overview
In its core idea ownCA is similar to [easy-rsa](https://github.com/OpenVPN/easy-rsa) project. The major difference between them is that easy-rsa is a CLI utility, whereas ownCA is a web-based tool.

# Use Cases
* Any place where certificates are required / need to be generated
* A network with limited number of computers that need to intercommunicate with each other using a secured, encrypted channel (no need to sign with a real CA).
* Companies with a limited budget for security and website protection
* Networks with the following configuration: 
  * Web Server (for SSL)
  * OpenVPN (for authorization + encrypted connection)
  * mail (for authorization + encrypted connection)

# Benefits
* Free solution
* Unlimited internal/private use
* Personal trust issuing authority

# References
* [easy-rsa](https://github.com/OpenVPN/easy-rsa)
* [Main Module](https://github.com/pyca/pyopenssl)
* [Django Framework](https://github.com/django/django)

# License
For more information about License, please refer to the [LICENSE](LICENSE) file.
