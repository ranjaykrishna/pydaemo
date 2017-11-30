from .utils import create_header
from .utils import delete
from .utils import get
from .utils import get_from_pages
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
      An object containing the id of the project and the template id.
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

  def get_projects(self, max_count=None):
    """Lists all the projects created.

    Args:
      max_count: When set, it only retrieves max_count number of projects.

    Returns:
      A list of the projects.
    """
    results = get_from_pages(self.url + '/v1/projects/?account_type=requester',
                             self.header, max_count=max_count)
    return results

  def get_project(self, project_id):
    """Retrieves a particular project.

    Args:
      project_id: The id of the project.

    Returns:
      The details of that project.
    """
    resp = get(self.url + '/v1/projects/' + project_id + '/', self.header)
    return resp

  def destroy_project(self, project_id):
    """Destroys a project.

    Args:
      project_id: The id of the project to destroy.
    """
    delete(self.url + '/v1/projects/' + str(project_id) + '/', self.header)

  def publish_project(self, project_id):
    """Publishes a project.

    Args:
      project_id: The id of the project to publish.
    """
    post(self.url + '/v1/projects/' + str(project_id) + '/publish/', None, self.header)

  def get_tasks(self, project_id, max_count=None):
    """Gets all the tasks for a project.

    Args:
      project_id: The id of the project who's tasks we want to get.
      max_count: When set, it only retrieves max_count number of tasks.

    Returns:
      A list of tasks.
    """
    results = get_from_pages(
        self.url + '/v1/projects/' + str(project_id) + '/tasks/',
        self.header, max_count=max_count)
    return results

  def get_tasks(self, project_id):
    """Gets all the tasks associated with a project_id.

    Args:
      project_id: The id of the project to publish.

    Returns:
      A list of tasks.
    """
    resp = get(self.url + '/v1/tasks/?project_id=' + project_id, self.header)
    return resp

  def get_task(self, task_id):
    """Get a specific task.

    Args:
      task_id: The id of the task we want to get.

    Returns:
      The task resource.
    """
    resp = get(self.url + '/v1/tasks/' + task_id + '/', self.header)
    return resp

  def create_task(self, project_id, data, price=None):
    """Creates a new task for a project.

    Args:
      project_id: The id of the project for which we want to create a task.
      data: The data associated with this task.
      price: optional price of the task. Projects already have a default price.

    Returns:
      The task_id of the newly created task.
    """
    data = {'data': data}
    if price is not None:
      data['price'] = price
    resp = post(self.url + '/v1/tasks/?project_id=' + project_id,
                data, self.header)
    return resp['id']

  def destroy_task(self, task_id):
    """Delete a task.

    Args:
      task_id: The id of the task to delete.
    """
    delete(self.url + '/v1/tasks/' + task_id + '/',  self.header)

  def get_task_results(self, task_id):
    """Get the results for all the assignments for a task.

    Args:
      task_id: The id of the task we want results for.

    Returns:
      A list of the assignment results.
    """
    results = get_from_pages(
        self.url + '/v1/tasks/' + task_id + '/assignment-results/',
        self.header)
    return results

  def get_assignments(self, task_id):
    """Get all the assignments associated with a task.

    Args:
      task_id: The id of the task who's assignments we want.

    Returns:
      A list of assignment resouces.
    """
    results = get_from_pages(
        self.url + '/v1/assignments/?task_id=' + task_id,
        self.header)
    return results

  def get_assignment(self, assignment_id):
    """Get a specific assignment_id.

    Args:
      assignment_id: The id of the assignment we want to get.

    Returns:
      An assignment resource.
    """
    resp = get(self.url + '/v1/assignments/' + assignment_id + '/', self.header)
    return resp

  def approve_assignment(self, assignment_id):
    """Approve an assignment.

    Args:
      assignment_id: The id of the assignment we want to approve.
    """
    resp = post(self.url + '/v1/assignments/' + assignment_id + '/approve/',
                None, self.header)
    return resp

  def return_assignment(self, assignment_id):
    """Return an assignment.

    Args:
      assignment_id: The id of the assignment we want to return.
    """
    resp = post(self.url + '/v1/assignments/' + assignment_id + '/return/',
                None, self.header)
    return resp

  def reject_assignment(self, assignment_id):
    """Reject an assignment.

    Args:
      assignment_id: The id of the assignment we want to reject.
    """
    resp = post(self.url + '/v1/assignments/' + assignment_id + '/reject/',
                None, self.header)
    return resp

  def get_templates(self):
    """Get all the templates created.

    Returns:
      A list of template resources.
    """
    results = get_from_pages(self.url + '/v1/templates/', self.header)
    return results

  def get_template(self, template_id):
    """Get a specific template.

    Args:
      template_id: The id of the template we want to get.

    Returns:
      A template resource.
    """
    resp = get(self.url + '/v1/templates/' + template_id + '/', self.header)
    return resp

  def create_template(self, name, items):
    """Create a template.

    Args:
      name: The name of the template.
      items: a list of template item resources.

    Returns:
      The template id.
    """
    data = {'name': name, 'items': items}
    resp = post(self.url + '/v1/templates/', data, self.header)
    return resp['id']

  def get_template_items(self, template_id):
    """Get all the template_items in a template.

    Args:
      template_id: The id of the template who's items we want.

    Returns:
      A list of template item resources.
    """
    results = get_from_pages(
        self.url + '/v1/templates-items/?template_id=' + template_id,
        self.header)
    return results

  def get_template_item(self, template_item_id):
    """Get a specific template item id.

    Args:
      template_item_id: The id of the template item we want.

    Returns:
      A template item resource.
    """
    resp = get(self.url + '/v1/template-items/' + template_item_id + '/',
               self.header)

  def create_template_item(self, name, item_type, sub_type, predecessor,
                           required, template, question_value,
                           max_length=None, min_length = None,
                           placeholder=None, src=None,
                           layout=None, shuffle=None,
                           options=None):
    """Creates a template item.

    Args:
      name: The name of the item.
      item_type: One of `text, instructions, file_upload, iframe, audio, image,
        radio, select_list, checkbox`.
      sub_type: can be `number, text_area and text` if type == `text`.
      predecessor: The previous template item's id.
      template: The id of the template that the item belong to.
      question_value: header to be added at the top of the item.
      max_length: Optional maximum number of characters that workers can type.
      min_length: Optional minimum number of characters that workers can type.
      placeholder: Optional placeholder for `text` field.
      src: Source for `iframe, audio or image` types.
      layout: Required for `checkbox, radio or select_list`. One of
        `row or column`.
      shuffle: Required True or False for `checkbox, radio or select_list`.
      options: A list of objects containing `value` and `position` for
        `checkbox, radio and select_list`.

    Returns:
      The id of the created template_item.
    """
    data = {'name': name,
            'type': item_type,
            'sub_type': sub_type,
            'predecessor': predecessor,
            'required': required,
            'template': template,
            'aux_attributes': {
              'question': {'value': question_value, 'data_source': None}}}
    if max_length is not None:
      data['aux_attributes']['max_length'] = max_length
    if min_length is not None:
      data['aux_attributes']['min_length'] = min_length
    if placeholder is not None:
      data['aux_attributes']['placeholder'] = placeholder
    if item_type in ['iframe', 'audio', 'image']:
      if src is None:
        raise ValueError('src must NOT be None when type is iframe, audio or image')
      data['aux_attributes']['src'] = src
    if item_type in ['checkbox', 'radio', 'select_list']:
      if layout is None or shuffle is None or options is None:
        raise ValueError('layout, shuffle and options must be set for checkbox, '
                         'radio and select_list')
      data['aux_attributes']['layout'] = layout
      data['aux_attributes']['shuffle_options'] = shuffle
      data['aux_attributes']['options'] = options
    resp = post(self.url + '/v1/template-items/', data, self.header)
    return resp['id']

  def destroy_template_item(self, template_item_id):
    """Delete a template item.

    Args:
      template_item_id: The id of the template item we want to delete.
    """
    delete(self.url + '/v1/template-items/' + template_item_id + '/', self.header)
