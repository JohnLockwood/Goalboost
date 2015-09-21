from flask.ext.login import UserMixin
from alguito.model.entities.userentity import UserEntity
import alguito.app as app

class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password

    #def __init__(self, username):
    #    self.username = username

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        if (self.password is not None):
            u = UserEntity(email=self.id, password = self.password)
            return u.verify_password(self.password)
        else:
            return True

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def get(cls,id):
        userEntity = app.db.session.query(UserEntity).filter(UserEntity.email == id).one()
        return User(userEntity.email, None)

'''
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None
'''
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None

#@app.route("/",methods=["GET"])
#def index():
#    return Response(response="Hello World!",status=200)


#@app.route("/protected/",methods=["GET"])
#@login_required
#def protected():
#    return Response(response="Hello Protected World!", status=200)