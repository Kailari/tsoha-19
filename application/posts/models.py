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
    def get_posts_for_user_wall(user_id, older_than, limit=-1):
        stmt = text("SELECT "
                    " Post.id AS post_id,"
                    " Post.owner_id AS poster_id,"
                    " Poster.name AS poster_name,"
                    " WallOwner.id AS wall_owner_id,"
                    " WallOwner.name AS wall_owner_name,"
                    " Post.date_created AS date_created,"
                    " Post.date_modified AS date_modified,"
                    " Post.content AS content,"
                    " COUNT(Comment.id) AS comment_count"
                    " FROM Post"
                    "  LEFT JOIN Comment ON Comment.post_id = Post.id"
                    "  INNER JOIN Account AS Poster ON Poster.id = Post.owner_id"
                    "  INNER JOIN Wall ON Wall.id = Post.wall_id"
                    "  INNER JOIN Account AS WallOwner ON WallOwner.id = Wall.id"
                    " WHERE WallOwner.id = :user_id"
                    "   AND Post.date_created < CAST(:older_than AS timestamp)"
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
                "comment_count": row["comment_count"],
            })
        return posts

    @staticmethod
    def get_posts_for_user_feed(user_id, older_than, limit=-1):
        stmt = text("SELECT "
                    "  Post.id AS post_id"
                    ", PostedBy.id AS postedby_id"
                    ", PostedBy.name AS postedby_name"
                    ", WallOwner.id AS wall_owner_id"
                    ", WallOwner.name AS wall_owner_name"
                    ", Post.date_created AS date_created"
                    ", Post.date_modified AS date_modified"
                    ", Post.content AS content"
                    ", (SELECT COUNT(Comment.id) AS comment_count"
                    "   FROM Comment "
                    "   WHERE Comment.post_id = Post.id"
                    "  )"
                    " FROM Post"
                    "  INNER JOIN Wall ON Wall.id = Post.wall_id"
                    "  INNER JOIN Account AS PostedBy ON Post.owner_id = PostedBy.id"
                    "  INNER JOIN Account AS WallOwner ON WallOwner.id = Wall.id"
                    # Owner check is needed to prevent other users' subscriptions from 
                    # creating duplicate lines in the results. Avoids having to add 
                    # a GROUP BY clause. Needs to be a left join to keep posts received
                    # without a subscription (e.g. posts from user itself) in the results.
                    "  LEFT JOIN Subscription ON Subscription.owner_id = :user_id"
                    "                        AND Subscription.wall_id = Wall.id"
                    # TODO: Should users automagically have a subscription on themselves?
                    #       Would avoid special-casing the owner here.
                    "  WHERE (Subscription.owner_id = :user_id OR Post.owner_id = :user_id OR Post.wall_id = :user_wall_id)"
                    "    AND Post.date_created < CAST(:older_than AS timestamp)"
                    "  ORDER BY Post.date_created DESC" +
                    ("  LIMIT :limit" if limit > 0 else "")
                    ).params(user_id=user_id, user_wall_id=user_id, older_than=str(older_than), limit=limit)
        res = db.engine.execute(stmt)

        posts = []
        for row in res:
            posts.append({
                "post_id": row["post_id"],
                "poster_id": row["postedby_id"],
                "poster_name": row["postedby_name"],
                "wall_owner_id": row["wall_owner_id"],
                "wall_owner_name": row["wall_owner_name"],
                "date_created": row["date_created"],
                "date_modified": row["date_modified"],
                "content": row["content"],
                "comment_count": row["comment_count"],
            })
        return posts
