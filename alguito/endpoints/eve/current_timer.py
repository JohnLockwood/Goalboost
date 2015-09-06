'''
current_timer_schema = {
    'start': {
        'type': 'datetime',
        'required': True
    },
    'length': {
        'type': 'integer',
        'min': 0,
        'required': False
    },
    'notes': {
        'type': 'string',
        'required': False
    }
}

current_timer = {
    'url': 'people/<regex("[a-f0-9]{24}"):_id>/timer',
    # em_title': 'timer',


    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': current_timer_schema
}
'''
