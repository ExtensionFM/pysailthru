#! /usr/bin/env python
#
# sailthru - implementing with a quickness


__doc__ = """Python bindings for the Sailthru API
(pysailthru - courtesy of ExtensionFM)

For more information, see

Home Page: http://github.com/extensionfm/pysailthru
Developer: http://docs.sailthru.com/api
"""

import rocket
from rocket.utils import sign_sorted_values

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
            ('options', rocket.json, ['optional']),
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

# Builds FUNCTIONS into actual objects and inserts them into globals()
rocket.generate_proxies(FUNCTIONS,
                        _get_api_docstring,
                        foreign_globals=globals())

class BlastProxy(BlastProxy):
    """Special proxy for handling the optional variables of 'blast.post'"""

    def post(self, **kwargs):
        """Sailthru call. See http://docs.sailthru.com/api/blast#%post-mode

        This call accepts many optional arguments. Instead of handling each
        one, I check for a general 'options' dict and expand those options
        by adding them to kwargs before the dynamic proxy is called.

        This approach isn't necessary for Rocket, but it demonstrates how you
        can override the IDL's generated calls for special handling.
        """
        if kwargs.has_key('options'):
            for o in kwargs['options']:
                kwargs[o] = kwargs['options'][o]
            kwargs.remove('options')
        return super(BlastProxy, self).post(**kwargs)


########################################
# API class implementation #############
########################################

class Sailthru(rocket.Rocket):
    """Provides access to the Sailthru API.

    Initialize with api_key and api_secret_key, both available from
    sailthru
    """
    def __init__(self, *args, **kwargs):
        super(Sailthru, self).__init__(FUNCTIONS, api_url=API_URL,
                                       *args, **kwargs)

    def check_error(self, response):
        """Checks if the given API response is an error, and then raises
        the appropriate exception.
        """
        if type(response) is dict and response.has_key('error'):
            raise rocket.RocketAPIError(response['error'], response['errormsg'])


    def build_query_args(self, *args, **kwargs):
        """Overrides Rocket's build_query_arg to set signing_alg to
        sign_sorted_values
        """
        return super(Sailthru, self).build_query_args(signing_alg=sign_sorted_values,
                                                      *args, **kwargs)
    
        
    def gen_query_url(self, url, function, format=None, method=None, get_args=None):
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
