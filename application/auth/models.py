from application import db
from application.models import WithIDAndDateCreated

from sqlalchemy import text


class User(WithIDAndDateCreated):
    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password_hash = db.Column(db.String(144), nullable=False)

    posts = db.relationship("Post", backref='owner', lazy=True)

    def __init__(self, name, username, password_hash):
        self.name = name
        self.username = username
        self.password_hash = password_hash

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def find_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def user_with_username_exists(username):
        stmt = text("SELECT CASE WHEN EXISTS ("
                    " SELECT *"
                    " FROM account"
                    " WHERE account.username = :username"
                    ")"
                    "THEN CAST(1 AS BIT)"
                    "ELSE CAST(0 AS BIT) END"
                    ).params(username=username)
        res = db.engine.execute(stmt).first()
        print("found: {}".format(res[0]) + " =================================================================================================================")
        return res[0] == 1
        
