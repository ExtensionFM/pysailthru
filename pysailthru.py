#! /usr/bin/env python
#
# sailthru - implementing with a quickness


__doc__ = """Python bindings for the Sailthru API
(pysailthru - courtesy of ExtensionFM)

For more information, see

Home Page: http://github.com/extensionfm/pysailthru
Developer: http://docs.sailthru.com/api

Pysailthru has one external dependency: simplejson

http://undefined.org/python/#simplejson to download it
    or
use pip install simplejson
"""

import rocket


########################################
# Settings #############################
########################################

VERSION = '0.1'

API_URL = 'http://api.sailthru.com'
API_URL_SECURE = None

API_DOCSTRING = '"""Sailthru call. See http://docs.sailthru.com/api/%s#%s-mode"""'

def _get_api_docstring(namespace, function):
    """The sailthru api docs are stored such that the namespace has
    a url and each function is listed sequentially on the namespace doc.
    """
    return API_DOCSTRING % (namespace, function)


########################################
# API implementation details ###########
########################################

# IDL for the API
FUNCTIONS = {
    'email': {
        'get': [
            ('email', str, []),
        ],
        'post': [
            ('email', str, []),
            ('vars', rocket.json, ['optional']),
            ('lists', rocket.json, ['optional']),
            ('templates', rocket.json, ['optional']),
        ],
    },
    'send': {
        'get': [
            ('send_id', str, []),
        ],
        'post': [
            ('template', str, []),
            ('email', str, []),
            ('vars', rocket.json, ['optional']),
            ('options', rocket.json, ['optional']),
            ('schedule_time', str, ['optional']),
        ],
        'delete': [
            ('send_id', str, []),
        ],
    },
    'blast': {
        'get': [
            ('blast_id', str, []),
        ],
        'post': [
            ('name', str, []),
            ('list', str, []),
            ('schedule_time', str, []),
            ('from_name', str, []),
            ('from_email', str, []),
            ('subject', str, []),
            ('content_html', str, []),
            ('context_html', str, []),
            ('options', rocket.json, []),
        ],
    },
    'template': {
        'get': [
            ('template', str, []),
        ],
    },
    'list': {
        'get': [
            ('list', str, []),
        ],
        'post': [
            ('list', str, []),
            ('emails', list, []),
        ],
        'delete': [
            ('list', str, []),
        ],
    },
    'contacts': {
        'post': [
            ('email', str, []),
            ('password', str, []),
            ('names', int, ['optional']),
        ],
    },
}

rocket.generate_proxies(FUNCTIONS, _get_api_docstring)


########################################
# API class implementation #############
########################################

class Sailthru(rocket.Rocket):
    """Provides access to the Sailthru API.

    Initialize with api_key and api_secret_key, both available from
    sailthru
    """
    def __init__(self, *args, **kwargs):
        self.function_list = FUNCTIONS
        super(Sailthru, self).__init__(*args, **kwargs)
        self.client = 'sailthru'
        self.api_url = API_URL

    def check_error(self, response):
        """Checks if the given API response is an error, and then raises
        the appropriate exception.
        """
        if type(response) is dict and response.has_key('error'):
            raise rocket.RocketAPIError(response['error'], response['errormsg'])


    def build_query_args(self, *args, **kwargs):
        """Overrides Rocket's build_query_arg to use _get_sorted_value_hash
        instead
        """
        signing_alg = self._get_sorted_value_hash
        return super(Sailthru, self).build_query_args(signing_alg=signing_alg,
                                                      *args, **kwargs)
    
        
    def gen_query_url(self, url, function, format=None, get_args=None):
        """Sailthru urls look like 'url/function'.

        Example: http://api.sailthru.com/email
        """
        return '%s/%s' % (url, function)


if __name__ == '__main__':
    api_key = ''
    api_secret_key = ''
    email = 'ih@ve.one'

    sailthru = Sailthru(api_key, api_secret_key)

    email = sailthru.email.get(email)
    print email
