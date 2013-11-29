from api_key import *
APIS = { 'plos'       : {
                          'url': "http://alm.plos.org/api/v3/articles",
                          'key': API_KEY.get('plos')
                        },
         'ojs'        : {
                          'url': None,
                          'key': API_KEY.get('ojs')
                        },
         'copernicus' : {
                          'url': None,
                          'key': API_KEY.get('copernicus')
                        }}