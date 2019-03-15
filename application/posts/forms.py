from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    content = StringField("Content",
                          widget=TextArea(),
                          validators=[
                              validators.Length(
                                  min=1,
                                  max=255,
                                  message="Post length must be 1 to 255 characters")])

    class Meta:
        csrf = False
