"""Contains helper functions for pydaemo.
"""


import json
import os
import requests


def create_header(credentials):
  """Creates the header dictionary used in all API calls.

  Args:
    credentials: An object containing 'access_token'.

  Returns:
    A dictionary to be used as the header for all API calls.
  """
  return {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + credentials['access_token']}


def make_request(method, url, data, headers):
  """Makes a request.

  Args:
    url: The URL to sent the request to.
    data: The data accompanying the request.
    headers: Headers to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  if data is None:
    resp = requests.request(method, url, headers=headers)
  else:
    resp = requests.request(method, url, json=data, headers=headers)
  if not resp.ok:
    resp.raise_for_status()
  return json.loads(resp.content)


def delete(url, data, headers):
  """Makes a DELETE request.

  Args:
    url: The URL to request to.
    data: The data accompanying the DELETE request.
    headers: Headers to be sent along with the request.

  Raises:
    HTTPError is the request fails.
  """
  requests.request('DELETE', url, headers=headers)



def post(url, data, headers):
  """Makes a POST request.

  Args:
    url: The URL to post to.
    data: The data accompanying the POST request.
    headers: Headers to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  return make_request('POST', url, data, headers)


def get(url, headers):
  """Makes a GET request.

  Args:
    url: The URL to get from.
    headers: Headers to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  return make_request('GET', url, None, headers)


def load_credentials(location):
  """Loads the credentials.

  Args:
    location: Path to file that contains the credentials.

  Raises:
    FileNotFoundError is the credentials don't exit.

  Returns:
    An object containing 'client_id', 'access_token' and 'refresh_token'.
  """
  if location is None:
    raise FileNotFoundError('No credential file specified.')
  elif not os.path.exists(location):
    raise FileNotFoundError('No such credential file: {}.'.format(location))
  return json.load(open(location, 'r'))


def save_credentials(credentials, location):
  """Saves the credentials.

  Args:
    credentials: An object containing 'client_id', 'refresh_token' and
      'access_token'.
    location: Path to file to store the credentials.

  Raises:
    FileNotFoundError is the credentials don't exit.
  """
  if location is None:
    raise FileNotFoundError('No credential file specified.')
  elif not os.path.exists(location):
    raise FileNotFoundError('No such credential file: {}.'.format(location))
  json.dump(credentials, open(location, 'w'))
