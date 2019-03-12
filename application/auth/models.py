from application import db
from application.models import WithIDAndDateCreated

class User(WithIDAndDateCreated):
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)

    def __init__(self, name, username, password_hash):
        self.name = name
        self.username = username
        self.password = password_hash
