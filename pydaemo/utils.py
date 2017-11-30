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


def make_request(method, url, data, header):
  """Makes a request.

  Args:
    url: The URL to sent the request to.
    data: The data accompanying the request.
    header: header to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  if data is None:
    resp = requests.request(method, url, headers=header)
  else:
    resp = requests.request(method, url, json=data, headers=header)
  if not resp.ok:
    resp.raise_for_status()
  return json.loads(resp.content)


def delete(url, header):
  """Makes a DELETE request.

  Args:
    url: The URL to request to.
    header: header to be sent along with the request.

  Raises:
    HTTPError is the request fails.
  """
  requests.request('DELETE', url, headers=header)



def post(url, data, header):
  """Makes a POST request.

  Args:
    url: The URL to post to.
    data: The data accompanying the POST request.
    header: header to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  return make_request('POST', url, data, header)


def get(url, header):
  """Makes a GET request.

  Args:
    url: The URL to get from.
    header: header to be sent along with the request.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  return make_request('GET', url, None, header)


def get_from_pages(url, header, max_count=None):
  """Get all the results from a paginated endpoint.

  Args:
    url: The URL to get from.
    header: header to be sent along with the request.
    max_count: Maximum number of results to get.

  Raises:
    HTTPError is the request fails.

  Returns:
    The response returned from the request.
  """
  results = []
  total = 0
  while url is not None:
    resp = get(url, header)
    results.extend(resp['results'])
    url = resp['next']
    total += resp['count']
    if max_count is not None and total >= max_count:
      break
  return results


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
