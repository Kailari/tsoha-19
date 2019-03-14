from application import db
from application.models import WithIDAndDatesCreatedAndModified
from sqlalchemy import text
import datetime
import os


class Post(WithIDAndDatesCreatedAndModified):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    owner_id = db.Column(db.Integer,
                         db.ForeignKey('account.id'),
                         nullable=False)

    wall_id = db.Column(db.Integer,
                        db.ForeignKey('wall.id'),
                        nullable=False)

    comments = db.relationship("Comment", backref='post', lazy=True)

    def __init__(self, content, owner_id, wall_id):
        super().__init__()
        self.content = content
        self.wall_id = wall_id
        self.owner_id = owner_id

    @staticmethod
    def get_posts_for_user_wall(user_id, older_than=None, limit=-1):
        if older_than == None:
            # Ugly hack to make sure new posts are considered "new enough" to be selected
            # If pagination is implemented, this can be discarded
            older_than = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)

        if os.environ.get("HEROKU"):
            stmt_where_date = "WHERE Post.date_created <= CAST(:older_than AS timestamp)"
        else:
            stmt_where_date = "WHERE Post.date_created <= Datetime(:older_than)"

        stmt = text("SELECT "
                    " Post.id AS post_id,"
                    " Post.owner_id AS poster_id,"
                    " Poster.name AS poster_name,"
                    " Post.date_created AS date_created,"
                    " Post.date_modified AS date_modified,"
                    " Post.content AS content"
                    " FROM Account"
                    "  INNER JOIN Wall ON Wall.id = :user_id"
                    "  INNER JOIN Post ON Post.wall_id = Wall.id"
                    "  INNER JOIN Account AS Poster ON Poster.id = Post.owner_id"
                    + stmt_where_date +
                    "  GROUP BY Post.id, Poster.name"
                    "  ORDER BY Post.date_created DESC" +
                    ("  LIMIT :limit" if limit > 0 else "")
                    ).params(user_id=user_id, older_than=str(older_than), limit=limit)
        res = db.engine.execute(stmt)

        posts = []
        for row in res:
            posts.append({
                "post_id": row["post_id"],
                "poster_id": row["poster_id"],
                "poster_name": row["poster_name"],
                "date_created": datetime.datetime.strptime(row["date_created"], "%Y-%m-%d %H:%M:%S.%f"),
                "date_modified": datetime.datetime.strptime(row["date_modified"], "%Y-%m-%d %H:%M:%S.%f"),
                "content": row["content"],
            })
        return posts
