from flask_wtf import FlaskForm
from wtforms import StringField, validators


class SearchForm(FlaskForm):
    name_filter = StringField("Filter",
                              validators=[
                                  validators.Length(
                                      min=1,
                                      max=100,
                                      message="Search term must be between 1 to 100 character long")])

    class Meta:
        csrf = False
