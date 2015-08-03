teams_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'name': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 80,
        'unique': 'True'
    }
}



teams = {
    # Default 'item_title': 'team',


    # by default the standard item entry point is defined as
    # '/teams/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/teams/name'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'name'
    },

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': teams_schema
}

