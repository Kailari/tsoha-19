from application import db
from application.models import WithIDAndDateCreated

# Make sure Wall is created before User so that trigger creation won't fail
from application.wall.models import Wall

from sqlalchemy import text


class User(WithIDAndDateCreated):
    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password_hash = db.Column(db.String(144), nullable=False)

    posts = db.relationship("Post", backref='owner', lazy=True)
    subscriptions = db.relationship("Subscription", backref='user', lazy=True)
    wall = db.relationship("Wall", backref='owner', uselist=False, lazy=True)

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
    def find_user_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def user_with_username_exists(username):
        stmt = text("SELECT CASE WHEN EXISTS ("
                    " SELECT *"
                    " FROM account"
                    " WHERE account.username = :username"
                    ")"
                    "THEN CAST(1 AS INTEGER)"
                    "ELSE CAST(0 AS INTEGER) END"
                    ).params(username=username)
        res = db.engine.execute(stmt).first()
        return res[0] == 1


# Create trigger for adding wall for the user automatically


def create_account_triggers():
    db.engine.execute("""
    CREATE TRIGGER create_wall_for_user 
    AFTER INSERT ON Account
    BEGIN
        INSERT INTO Wall (id) VALUES (NEW.id);
    END;
    """)
