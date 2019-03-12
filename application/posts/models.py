from application import db
from sqlalchemy import text
from application.models import WithIDAndDatesCreatedAndModified
import os

class Post(WithIDAndDatesCreatedAndModified):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    owner_id = db.Column(db.Integer,
                         db.ForeignKey('account.id'),
                         nullable=False)

    def __init__(self, content):
        super().__init__()
        self.content = content
