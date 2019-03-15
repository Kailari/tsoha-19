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
        self.owner_id = owner_id
        self.wall_id = wall_id

    @staticmethod
    def get_posts_for_user_wall(user_id, older_than=None, limit=-1):
        if older_than == None:
            # Ugly hack to make sure new posts are considered "new enough" to be selected
            # If pagination is implemented, this can be discarded
            older_than = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)

        stmt = text("SELECT "
                    " Post.id AS post_id,"
                    " Post.owner_id AS poster_id,"
                    " Poster.name AS poster_name,"
                    " WallOwner.id AS wall_owner_id,"
                    " WallOwner.name AS wall_owner_name,"
                    " Post.date_created AS date_created,"
                    " Post.date_modified AS date_modified,"
                    " Post.content AS content"
                    " FROM Post"
                    "  INNER JOIN Account AS Poster ON Poster.id = Post.owner_id"
                    "  INNER JOIN Wall ON Wall.id = Post.wall_id"
                    "  INNER JOIN Account AS WallOwner ON WallOwner.id = Wall.id"
                    " WHERE WallOwner.id = :user_id"
                    "   AND Post.date_created <= CAST(:older_than AS timestamp)"
                    "  GROUP BY Post.id, Poster.id, Poster.name, WallOwner.id"
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
                "wall_owner_id": row["wall_owner_id"],
                "wall_owner_name": row["wall_owner_name"],
                "date_created": row["date_created"],
                "date_modified": row["date_modified"],
                "content": row["content"],
            })
        return posts

    @staticmethod
    def get_posts_for_user_feed(user_id, older_than=None, limit=-1):
        if older_than == None:
            # Ugly hack to make sure new posts are considered "new enough" to be selected
            # If pagination is implemented, this can be discarded
            older_than = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)

        stmt = text("SELECT "
                    " Post.id AS post_id,"
                    " Poster.id AS poster_id,"
                    " Poster.name AS poster_name,"
                    " WallOwner.id AS wall_owner_id,"
                    " WallOwner.name AS wall_owner_name,"
                    " Post.date_created AS date_created,"
                    " Post.date_modified AS date_modified,"
                    " Post.content AS content"
                    " FROM Post"
                    "  LEFT JOIN Account AS Poster ON Post.owner_id = Poster.id"
                    "  LEFT JOIN Wall ON Wall.id = Post.wall_id"
                    "  LEFT JOIN Subscription ON Subscription.wall_id = Wall.id"
                    "  LEFT JOIN Account AS WallOwner ON WallOwner.id = Wall.id"
                    "  WHERE (Subscription.owner_id = :user_id OR Post.owner_id = :user_id OR Post.wall_id = :user_wall_id)"
                    "    AND Post.date_created <= CAST(:older_than AS timestamp)"
                    "  GROUP BY Post.id, Poster.id, Poster.name, WallOwner.id"
                    "  ORDER BY Post.date_created DESC" +
                    ("  LIMIT :limit" if limit > 0 else "")
                    ).params(user_id=user_id, user_wall_id=user_id, older_than=str(older_than), limit=limit)
        res = db.engine.execute(stmt)

        posts = []
        for row in res:
            posts.append({
                "post_id": row["post_id"],
                "poster_id": row["poster_id"],
                "poster_name": row["poster_name"],
                "wall_owner_id": row["wall_owner_id"],
                "wall_owner_name": row["wall_owner_name"],
                "date_created": row["date_created"],
                "date_modified": row["date_modified"],
                "content": row["content"],
            })
        return posts
