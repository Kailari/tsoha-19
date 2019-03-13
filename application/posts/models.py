from application import db
from application.models import WithIDAndDatesCreatedAndModified
from sqlalchemy import text
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
    def get_posts_for_user_wall(user_id):
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
                    "  GROUP BY Post.id"
                    ).params(user_id=user_id)
        res = db.engine.execute(stmt)

        posts = []
        for row in res:
            posts.append({
                "post_id": row["post_id"],
                "poster_id": row["poster_id"],
                "poster_name": row["poster_name"],
                "date_created": row["date_created"],
                "date_modified": row["date_modified"],
                "content": row["content"],
            })
        return posts
