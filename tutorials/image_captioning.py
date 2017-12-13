"""Create a image captioning task.
"""

from pydaemo import Daemo

if __name__=='__main__':
    # Let's say we need to caption the images in the following urls:
    urls = ['https://cs.stanford.edu/people/rak248/VG_100K/2322397.jpg',
            'https://cs.stanford.edu/people/rak248/VG_100K/2322398.jpg',
            'https://cs.stanford.edu/people/rak248/VG_100K/2322399.jpg']
    # Basic setup.
    daemo = Daemo(update_credentials=True)
    project = daemo.create_project(name='Image Captioning Project', price=0.2,
                                   template_name='Image Captioning Template',
                                   verbose=True)
    print('created project: ', project)

    # Let's assign a location for the image.
    question_name = 'image'
    question_type = 'image'
    question_subtype = None
    predecessor = None
    required = False
    question = 'An image you need to caption.'
    image = daemo.create_template_item(question_name, question_type,
                                         question_subtype, predecessor,
                                         required, project['template_id'],
                                         '', src='{{url}}',
                                         verbose=True)
    print('created image with id: ', image)

    # Next, we will create a text field.
    question_name = 'caption'
    question_type = 'text'
    question_subtype = 'text'
    predecessor = image
    required = True
    question = 'Caption the image.'
    placeholder = 'add your caption here...'
    caption = daemo.create_template_item(question_name, question_type,
                                         question_subtype, predecessor,
                                         required, project['template_id'],
                                         '', placeholder=placeholder,
                                         verbose=True)
    print('created caption with id: ', caption)

    # Let's create a task for a each url.
    for url in urls:
        daemo.create_task(project['id'], {'url': url}, verbose=True)

    # Finally, let's publish the project and check its status.
    daemo.publish_project(project['id'], verbose=True)
    print(daemo.get_project(project['id']))
