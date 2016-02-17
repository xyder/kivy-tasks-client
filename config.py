from views.tasks_list_view import convert_time

use_kv_file = False
form_input_formats = [
        {
            'label': 'Title',
            'key': 'title',
            'formatter': None
        },
        {
            'label': 'Description',
            'key': 'body',
            'formatter': None,
            'args': {
                'height': 105,
                'input_height': 70,
                'multiline': True
            }
        },
        {
            'label': 'Created Date',
            'key': 'created',
            'formatter': convert_time
        },
        {
            'label': 'Due Date',
            'key': 'due',
            'formatter': convert_time
        },
        {
            'label': 'Status',
            'key': 'state',
            'formatter': None
        }
    ]

# api urls
api_version = '1'
api_url_root = '/api/v%s' % api_version
api_url_start = '%s/tasks' % api_url_root
api_url_item = api_url_start + '/%s'
server_address = 'http://localhost:5000'
