from application import db
import datetime

# Base for db tables with
#  - id = integer primary key


class WithID(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer,
                   primary_key=True)

# Base for db tables with
#  - id             = integer primary key
#  - date_created   = datetime when entry was created


class WithIDAndDateCreated(WithID):
    __abstract__ = True

    date_created = db.Column(db.DateTime,
                             default=datetime.datetime.utcnow)

# Base for db tables with
#  - id             = integer primary key
#  - date_created   = datetime when entry was created
#  - date_modified  = datetime when entry was last modified


class WithIDAndDatesCreatedAndModified(WithIDAndDateCreated):
    __abstract__ = True

    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.utcnow,
                              onupdate=datetime.datetime.utcnow)

    def __init__(self):
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = self.date_created
