"""Create a simple survey.
"""

from pydaemo import Daemo

if __name__=='__main__':
    daemo = Daemo(update_credentials=True)
    project = daemo.create_project(name='Simple Survey Project', price=0.2,
                                   template_name='Simple Survey Template',
                                   verbose=True)
    print('created project: ', project)
    options = [{'value': 'yes', 'position': 0},
               {'value': 'no', 'position': 1}]

    # First let's create a radio button.
    question1 = daemo.create_template_item('Q1', 'radio', None, None,
                                           True, project['template_id'],
                                           'Isn\'t this survey easy?',
                                           layout='row', shuffle=False,
                                           options=options, verbose=True)
    print('created question1 with id: ', question1)

    # Next, we will create a text field.
    question2 = daemo.create_template_item('Q2', 'text', 'text', question1,
                                           False, project['template_id'],
                                           'Is there anything else you would '
                                           'like to say?',
                                           placeholder='placeholder',
                                           verbose=True)
    print('created question2 with id: ', question2)

    # Finally, let's create a dynamic question where we will pass in the
    # question as a data field.
    question3 = daemo.create_template_item('Q3', 'text', 'text', question2,
                                           False, project['template_id'],
                                           '{{dynamic_question}}',
                                           placeholder='placeholder',
                                           verbose=True)

    # Let's create a task for a worker to complete with the dynamic question.
    daemo.create_task(
        project['id'],
        {'dynamic_question': 'Woah, a dynamic question! '},
        verbose=True)

    # Finally, let's publish the project and check its status.
    daemo.publish_project(project['id'], verbose=True)
    print(daemo.get_project(project['id']))
