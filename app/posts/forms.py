from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length

CATEGORIES = [
    ("news", "news"),
    ("publication", "publication"),
    ("tech", "tech"),
    ("other", "other"),
]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField(
        "Content",
        render_kw={"rows": 6},
        validators=[DataRequired(), Length(min=1)]
    )
    is_active = BooleanField("Active Post")

    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now
    )

    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])

    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])

    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField("Submit")