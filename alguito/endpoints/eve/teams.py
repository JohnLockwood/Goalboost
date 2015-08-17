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

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    # most global settings can be overridden at resource level
    'item_methods': ['PUT', 'DELETE'],


    'schema': teams_schema
}

