from flask_wtf import FlaskForm
from wtforms import StringField

class PostForm(FlaskForm):
    content = StringField("Content")

    class Meta:
        csrf = False
