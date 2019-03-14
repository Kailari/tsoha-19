from application import db


class Wall(db.Model):
    id = db.Column(db.Integer,
                   db.ForeignKey('account.id'),
                   primary_key=True,
                   nullable=False)

    posts = db.relationship("Post", backref='wall', lazy=True)
    subscribers = db.relationship("Subscription", backref='wall', lazy=True)

    def __init__(self, owner_id):
        self.owner_id = owner_id


class Subscription(db.Model):
    owner_id = db.Column(db.Integer,
                         db.ForeignKey('account.id'),
                         primary_key=True,
                         nullable=False)
    wall_id = db.Column(db.Integer,
                        db.ForeignKey('wall.id'),
                        primary_key=True,
                        nullable=False)

    def __init__(self, owner_id, wall_id):
        self.owner_id = owner_id
        self.wall_id = wall_id
