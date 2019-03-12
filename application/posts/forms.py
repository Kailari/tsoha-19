from flask_wtf import FlaskForm
from wtforms import StringField, validators


class PostForm(FlaskForm):
    content = StringField("Content", [
        validators.Length(
            min=1, max=255, message="Post length must be 1 to 255 characters")])

    class Meta:
        csrf = False
