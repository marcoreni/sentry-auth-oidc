from __future__ import absolute_import, print_function

from django.conf import settings
import requests


AUTHORIZATION_ENDPOINT = getattr(settings, 'OIDC_AUTHORIZATION_ENDPOINT', None)
TOKEN_ENDPOINT = getattr(settings, 'OIDC_TOKEN_ENDPOINT', None)
CLIENT_ID = getattr(settings, 'OIDC_CLIENT_ID', None)
CLIENT_SECRET = getattr(settings, 'OIDC_CLIENT_SECRET', None)
USERINFO_ENDPOINT = getattr(settings, 'OIDC_USERINFO_ENDPOINT', None)
SCOPE = getattr(settings, 'OIDC_SCOPE', 'openid email')
DOMAIN_BLACKLIST = frozenset(getattr(settings, 'OIDC_DOMAIN_BLACKLIST', None) or [])
DOMAIN_WHITELIST = frozenset(getattr(settings, 'OIDC_DOMAIN_WHITELIST', None) or [])
WELL_KNOWN_SCHEME = "/.well-known/openid-configuration"
ERR_INVALID_RESPONSE = 'Unable to fetch user information from provider.  Please check the log.'
ERR_INVALID_DOMAIN = 'The domain for your email account (%s) is not allowed to authenticate with this provider.'
ISSUER = None


DATA_VERSION = '1'

OIDC_DOMAIN = getattr(settings, 'OIDC_DOMAIN', None)
if OIDC_DOMAIN:
    WELL_KNOWN_URL = OIDC_DOMAIN.strip("/") + WELL_KNOWN_SCHEME
    well_known_values = requests.get(WELL_KNOWN_URL, timeout=2.0).json()
    if well_known_values:
        USERINFO_ENDPOINT = well_known_values['userinfo_endpoint']
        AUTHORIZATION_ENDPOINT = well_known_values['authorization_endpoint']
        TOKEN_ENDPOINT = well_known_values['token_endpoint']
        ISSUER = well_known_values['issuer']


config_issuer = getattr(settings, 'OIDC_ISSUER', None)
if config_issuer:
    ISSUER = config_issuer
