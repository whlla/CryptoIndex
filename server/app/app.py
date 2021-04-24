import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore,\
    RoleMixin, UserMixin, auth_required, hash_password
from pymongo import MongoClient

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'aV-Wwe9kbu2mTW-EaE67rVhSjeHDvzbLcM0JaKUtMRc')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '116361912168258564841410194036833729473')

# app.config['MONGO_DB'] = 'crypto'
# app.config['MONGO_HOST'] = 'database'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_USERNAME'] = 'cryptoRW'
# app.config['MONGO_PASSWORD'] = 'cryptotestpls'

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'crypto',
#     'host': 'database',
#     'port': 27017,
#     'username': 'cryptoRW',
#     'password': 'cryptotestpls'
# }

mongoClient = MongoClient('mongodb://crpytoRW:cryptotestpls@database:27017/crypto')

app.config['MONGODB_SETTINGS'] = {
    'db': 'crypto',
    'host': "mongodb://crpytoRW:cryptotestpls@database:27017/crypto"
}
# app.config['MONGO_HOST'] = "mongodb://crpytoRW:cryptotestpls@database:27017/crypto"

db = MongoEngine(app)

def user_exists(email):
    user_doc = mongoClient.get_database('crypto').get_collection('user').find_one({'email': email})
    if user_doc:
        return True
    return False


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    fs_uniquifier = db.StringField(max_length=255)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create user to test
@app.before_first_request
def create_user():
    if not user_exists('buildtest@gmail.com'):
        user_datastore.create_user(email='buildtest@gmail.com', password=hash_password("test1234"))


@app.route('/')
@auth_required('basic')
def hello_world():
    try:
        client = MongoClient("mongodb://crpytoRW:cryptotestpls@database:27017/crypto")
        db = client.crypto
        doc = db.crypto.find_one({})
        return doc.get('status')
    except Exception as e:
        return ("Exception. {}".format(e))
        return 'Mongo failed'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
