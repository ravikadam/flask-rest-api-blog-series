from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Organisation(db.Document):
    name = db.StringField(required=True, unique=True)
    access_license = db.ListField(db.StringField(), required=True)
    logo_url = db.StringField(required=False, unique=False)

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    #movies = db.ListField(db.ReferenceField('Movie', reverse_delete_rule=db.PULL))
    org = db.ReferenceField('Organisation')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

#Organisation.register_delete_rule(User, 'added_by', db.CASCADE)