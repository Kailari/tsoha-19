from flask_wtf import FlaskForm
from wtforms import StringField, validators


class SearchForm(FlaskForm):
    name_filter = StringField("Filter",
                              validators=[
                                  validators.Length(
                                      min=1,
                                      message="Search term must be at least 1 character long")])

    class Meta:
        csrf = False
