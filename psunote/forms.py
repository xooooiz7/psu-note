from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from wtforms import Field, widgets, SelectMultipleField

import models


class TagListField(Field):
    widget = widgets.TextInput()

    def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.data = []

    def process_formdata(self, valuelist):
        data = []
        if valuelist:
            data = [x.strip() for x in valuelist[0].split(",")]

        if not self.remove_duplicates:
            self.data = data
            return

        self.data = []
        for d in data:
            if d not in self.data:
                self.data.append(d)

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""


BaseNoteForm = model_form(
    models.Note,
    base_class=FlaskForm,
    exclude=["created_date", "updated_date"],
    db_session=models.db.session
)



def get_tag_choices():
    # Import here to avoid circular import
    from models import Tag, db
    with db.session.no_autoflush:
        tags = db.session.query(Tag).order_by(Tag.name).all()
    return [(tag.name, tag.name) for tag in tags]

class NoteForm(BaseNoteForm):
    tags = SelectMultipleField(
        "Tags",
        choices=[],
        coerce=str,
        render_kw={"class": "form-select", "multiple": True}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags.choices = get_tag_choices()
