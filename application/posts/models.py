from application import db
from sqlalchemy import text
from application.models import WithIDAndDatesCreatedAndModified
import os

if os.environ.get("HEROKU"):
    get_all_stmt = text()
else:
    get_all_stmt = text("SELECT"
                        "")


class Post(WithIDAndDatesCreatedAndModified):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    owner_id = db.Column(db.Integer,
                         db.ForeignKey('account.id'),
                         nullable=False)

    def __init__(self, content):
        super().__init__()
        self.content = content
