"""Contains helper functions for pydaemo.
"""

from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from urllib import parse
from urllib import request

import json


def post(url, data):
  """Makes a POST request.

  Args:
    url: The URL to post to.
    data: The data accompanying the POST request.

  Returns:
    The response returned from the request.
  """
  data = parse.urlencode(data).encode()
  req =  request.Request(url, data=data) # this will make the method "POST"
  resp = request.urlopen(req)
  return resp


def load_credentials(location=None):
  """Loads the credentials.

  Args:
    location: Path to file that contains the credentials.

  Returns:
    An object containing 'client_id', 'access_token' and 'refresh_token'.
  """
  if location is None:
    raise FileNotFoundError('No credential file specified.')
  elif not os.exists(location):
    raise FileNotFoundError('No such credential file: {}.'.format(location))
  return json.load(open(location, 'r'))


def authenticate(url, credentials):
  """Use the credentials to do a oauth.

  Args:
    url: The url from which to request the token.
    credentials: An object containing 'client_id' and 'client_secret'.

  Returns:
    The token returned by server.
  """
  auth = HTTPBasicAuth(credentials['client_id'], credentials['client_secret'])
  client = BackendApplicationClient(client_id=credentials['client_id'])
  oauth = OAuth2Session(client=client)
  token = oauth.fetch_token(token_url=url,
                            client_id=client_id,
                            client_secret=client_secret)
  return token
