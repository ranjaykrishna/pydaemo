from .utils import create_header
from .utils import delete
from .utils import get
from .utils import load_credentials
from .utils import post


class Daemo(object):
  """Contains all the API functionality to interface with Daemo.
  """

  def __init__(self, credential_file='credentials.json', prod=False,
               update_credentials=False):
    """Constructor for Daemo.

    Args:
      credential_file: The location of the the credentials for the user's Daemo
        account.
      prod: Boolean that connects to production is True or sandbox if False.
      update_credentials: Boolean that refreshes the access_token if True.
    """
    self.credentials = load_credentials(credential_file)
    if update_credentials:
      self._update_credentials()
      save_credentials(self.credentials, credential_file)
    self.header = create_header(self.credentials)
    if prod:
      self.url = 'https://daemo.org'
    else:
      self.url = 'https://sandbox.daemo.org'

  def _update_credentials(self):
    """Uses the refresh token to update the access token.
    """
    data = {'grant_type': 'refresh_token',
            'client_id': self.credentials['client_id'],
            'refresh_token': self.credentials['refresh_token']}
    resp = post(self.url + '/api/oauth2-ng/token/', data,
                {'Content-Type': 'application/json'})
    self.credentials['access_token'] = resp['access_token']

  def create_project(self, name, price, template_name,
                     repetition=1, timeout=120):
    """Creates a new Daemo project.

    Args:
      name: Name of the new Project.
      price: Price of each task.
      template_name: Name of the template to use.
      repetition: How many assignments the task should have.
      timeout: Maximum time allocated before expiring the task.

    Returns:
      The response from the request.
    """
    if not (isinstance(name, str) and len(name) > 0):
      raise TypeError('\'name\' of project needs to be a non-empty string.')
    if price <= 0:
      raise TypeError('\'price\' needs to be a positive value.')
    data = {'name': name,
            'price': price,
            'repetition': repetition,
            'timeout': timeout,
            'template': {'name': template_name,
                         'items': []}}
    resp = post(self.url + '/v1/projects/', data, self.header)
    return resp

  def get_projects(self, max_projects=None):
    """Lists all the projects created.

    Returns:
      An object containing total number of projects and the list of projects.
    """
    total = 0
    results = []
    addr = self.url + '/v1/projects/?account_type=requester'
    while addr is not None:
      resp = get(addr, None, self.header)
      results.extend(resp['results'])
      total += resp['count']
      addr = resp['next']
      if max_projects is not None and total >= max_projects:
        break
    return {'count': total, 'results': results}

  def get_project(self, project_id):
    """Retrieves a particular project.

    Args:
      project_id: The id of the project.

    Returns:
      The details of that project.
    """
    resp = get(self.url + '/v1/projects/' + project_id + '/', None, self.header)
    return resp

  def destroy_project(self, project_id):
    """Destroys a project.

    Args:
      project_id: The id of the project to destroy.
    """
    delete(self.url + '/v1/projects/' + str(project_id) + '/', None, self.header)

  def publish_project(self, project_id):
    """Publishes a project.

    Args:
      project_id: The id of the project to publish.
    """
    post(self.url + '/v1/projects/' + str(project_id) + '/publish/', None, self.header)

  def get_tasks(self, project_id, max_tasks=None):
    """Gets all the tasks for a project.

    Returns:
      An object containing total number of tasks and the list of tasks.
    """
    total = 0
    results = []
    addr = self.url + '/v1/projects/' + str(project_id) + '/tasks/'
    while addr is not None:
      resp = get(addr, None, self.header)
      results.extend(resp['results'])
      total += resp['count']
      addr = resp['next']
      if max_projects is not None and total >= max_projects:
        break
    return {'count': total, 'results': results}
