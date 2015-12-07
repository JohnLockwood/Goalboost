from goalboost.model import db




class Project(db.Document):
    name = db.StringField(max_length = 255)

class Tag(db.Document):
    accountId = db.ObjectIdField(unique_with="name", required=True)
    name = db.StringField(max_length = 80, required = True)
    collectionName = db.StringField(max_length=80)
    collectionId = db.ObjectIdField(required=False)


