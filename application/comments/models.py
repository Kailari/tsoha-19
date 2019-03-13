from application import db
from application.models import WithIDAndDatesCreatedAndModified


class Comment(WithIDAndDatesCreatedAndModified):
    content = db.Column(db.String(255), nullable=False)

    owner_id = db.Column(db.Integer,
                         db.ForeignKey('account.id'),
                         nullable=False)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        nullable=False)

    def __init__(self, content, owner_id, post_id):
        super().__init__()
        self.content = content
        self.owner_id = owner_id
        self.post_id = post_id
