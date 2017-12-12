# PyDaemo
![PyDaemo logo](http://hci.stanford.edu/publications/2017/crowdresearch/logo.jpg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/ranjaykrishna/pydaemo/blob/master/LICENSE)

Python Wrapper for [Daemo](https://daemo.stanford.edu).

PyDaemo should allow you to create and manage all your crowdsourcing tasks for Daemo programmatically.

Read the documentations at [pydaemo.readthedocs.io](http://pydaemo.readthedocs.io)

## Download and Installation.

To download and install PyDaemo, run the following command:
```
pip install pydaemo
```

To install from source, run:
```
git clone https://github.com/ranjaykrishna/pydaemo.git
cd pydaemo
python setup.py install
```

## Getting started with PyDaemo.
The first step to use the API is to download your credentials so that you have permissions to communicate with Daemo. Download the access tokens as a JSON file by navigating to your Daemo Profile and clicking "Get Credentials" under the menu in your profile.

Ensure that the credentials you obtain contain a `client_id`, `access_token` and `refresh_token`. Create and save your credentials in `credentials.json` file. Let's explore the API with two use cases. In the first example below, we will use PyDaemo to create, launch and collect surveys filled in by crowd workers.

### Let's create a simple survey project.
Let's create a simple survey task with 3 questions:
1. A radio button question.
2. A text question.
3. A dynamic question who's question will be filled in dynamically for each task.

The script to automatically create such a task is located here: `scripts/simple_survey.py`.

First, let's intialize the Daemo's api endpoints.
```
daemo = Daemo(update_credentials=False)
```

Next let's create a project and a template.
```
project = daemo.create_project(name='Simple Survey Project', price=0.2,
                               template_name='Simple Survey Template')
print('created project: ', project)
> created project: {"id": 37, "template_id": 14}
```

Now, we will add the first question: A radio button where the options are `yes` and `no` laid out in a `row`. We want to ask the question `Isn't this survey east?`. Let's make sure that this question is a required question.
```
options = [{'value': 'yes', 'position': 0},
           {'value': 'no', 'position': 1}]
required = True
question = 'Isn\'t this survey easy?',
question_subtype = None
question_name = 'Q1'
question_type = 'radio'
predecessor = None
question1 = daemo.create_template_item(question_name, question_type, 
                                       question_subtype, predecessor,
                                       required, project['template_id'],
                                       question, layout='row', shuffle=False,
                                       options=options)
print('created question1 with id: ', question1)
> created question1 with id: 10
```

Next, let's create the question with a text field. We are asking `Is there anything else you would like to say?`. We are setting this question to be optional (not required).
```
required = False
question = 'Is there anything else you would like to say?'
question_subtype = 'text'
question_name = 'Q2'
question_type = 'text'
predecessor = question1
question2 = daemo.create_template_item(question_name, question_type,
                                       question_subtype, predecessor,
                                       required, project['template_id'],
                                       question,
                                       placeholder='placeholder')
print('created question2 with id: ', question2)
> created question2 with id: 11
```

The third question is going to be a dynamic question that will be set from the data passed in. This allows requestors to customize each task. To create such a task, we simply need to set the `question` to be `{{VARIABLE}}` and make sure that we create a task with a dictionary  containing the header `VARIABLE`. Here is what it will look like in code:
```
required = False
question = '{{dynamic_question}}'
question_subtype = 'text'
question_name = 'Q3'
question_type = 'text'
predecessor = question2
question3 = daemo.create_template_item(question_name, question_type,
                                       question_subtype, predecessor,
                                       required, project['template_id'],
                                       question,
                                       placeholder='placeholder')
print('created question3 with id: ', question3)
> created question3 with id: 14
```

And we can create a task like this:
```
daemo.create_task(
    project['id'],
    {'dynamic_question': 'Woah, a dynamic question!'})
```

Finally, we can publish the project and wait for workers to complete the task:
```
response = daemo.publish_project(project['id'])
print(response)
> {"message": "Project :projectName successfully published"}
```


### Let's get more advanced task where we ask workers to caption images. 
Coming soon.

### How to retrieve the results and approve work.
Coming soon.

### Tutorial for using custom iframes to create tasks.
Coming soon.

### Contributing to the repository.
We gladly welcome contributions that improve the API or even provide additional tutorials that demonstrate how to use PyDaemo. Create a fork of this repository and send a pull request.
