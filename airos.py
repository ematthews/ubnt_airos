#!/usr/bin/env python

import json
import requests

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass

class AirOS(object):
    _host = None
    _username = None
    _password = None
    _initial_page = ''
    _login_page = 'login.cgi'
    _status_page = 'status.cgi'
    status = None

    
    def __repr__(self):
        return str(self.status)


    def __init__(self, host=None, username=None, password=None):
        self._host = host
        self._username = username
        self._password = password 
        status_page = self.assemble_url()
        self.status = self.get_status()
        return 


    def assemble_url(self):
        status_url = "https://{host}/{page}".format(
            host=self._host,
            page=self._status_page,
        )
        return status_url


    def assemble_payload(self):
        payload = {
            'uri': ('', "/{page}".format(page=self._status_page)),
            'username': ('', self._username),
            'password': ('', self._password),
            'submit': ('', 'Login'),
            'lang_changed': ('', 'no'),
        }

        return payload


    def get_status(self):
        initial_page = "https://{host}/{page}".format(host=self._host, page=self._initial_page)
        login_page = "https://{host}/{page}".format(host=self._host, page=self._login_page)
        mysession = requests.Session()

        # Initial page is requested in order to get an AIROS_SESSIONID value.
        content = mysession.get(initial_page, verify=False)

        # Now we have the cookies set, pass the multi-part POST request.
        payload = self.assemble_payload()
        content = mysession.post(login_page, files=payload, verify=False)
        myjson = content.json()

        return myjson
