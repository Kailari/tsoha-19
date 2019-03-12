from application import db

# Base for db tables with
#  - id = integer primary key


class WithID(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

# Base for db tables with
#  - id             = integer primary key
#  - date_created   = datetime when entry was created


class WithIDAndDateCreated(WithID):
    __abstract__ = True

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

# Base for db tables with
#  - id             = integer primary key
#  - date_created   = datetime when entry was created
#  - date_modified  = datetime when entry was last modified


class WithIDAndDatesCreatedAndModified(WithIDAndDateCreated):
    __abstract__ = True

    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
