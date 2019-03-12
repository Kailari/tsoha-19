from application import db
from application.models import WithIDAndDatesCreatedAndModified

class Post(WithIDAndDatesCreatedAndModified):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    def __init__(self, content):
        self.content = content
