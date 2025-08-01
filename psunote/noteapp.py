import flask

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


import flask
import models
import forms

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"
models.init_app(app)

# Home page: list all notes
@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(db.select(models.Note).order_by(models.Note.title)).scalars()
    return flask.render_template("index.html", notes=notes)

# Create note
@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if form.validate_on_submit():
        db = models.db
        note = models.Note()
        # populate_obj will not touch tags
        data = form.data.copy()
        data.pop('tags', None)
        for k, v in data.items():
            setattr(note, k, v)
        note.tags = []
        for tag_name in form.tags.data:
            tag = db.session.query(models.Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            if tag not in note.tags:
                note.tags.append(tag)
        db.session.add(note)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))
    return flask.render_template("notes-create.html", form=form, edit=False)

# Edit note
@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)
    form = forms.NoteForm(obj=note)
    if form.validate_on_submit():
        # populate_obj will not touch tags
        data = form.data.copy()
        data.pop('tags', None)
        for k, v in data.items():
            setattr(note, k, v)
        note.tags = []
        for tag_name in form.tags.data:
            tag = db.session.query(models.Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            if tag not in note.tags:
                note.tags.append(tag)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))
    form.tags.data = [tag.name for tag in note.tags]
    return flask.render_template("notes-create.html", form=form, edit=True)

# Delete note
@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)
    db.session.delete(note)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))

# View notes by tag
@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
    if not tag:
        flask.abort(404)
    notes = db.session.execute(db.select(models.Note).where(models.Note.tags.any(id=tag.id))).scalars()
    return flask.render_template("tags-view.html", tag_name=tag_name, notes=notes)

# List tags
@app.route("/tags", endpoint="tags_list")
def tags_list():
    db = models.db
    tags = db.session.execute(db.select(models.Tag).order_by(models.Tag.name)).scalars()
    return flask.render_template("tags-list.html", tags=tags)

# Add tag
@app.route("/tags/add", methods=["GET", "POST"])
def tags_add():
    db = models.db
    if flask.request.method == "POST":
        tag_name = flask.request.form.get("name")
        if tag_name:
            tag = db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
        return flask.redirect(flask.url_for("tags_list"))
    return flask.render_template("tags-add.html")

# Edit tag
@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    if flask.request.method == "POST":
        tag_name = flask.request.form.get("name")
        if tag_name:
            tag.name = tag_name
            db.session.commit()
            return flask.redirect(flask.url_for("tags_list"))
    return flask.render_template("tags-edit.html", tag=tag)

# Delete tag
@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    db.session.delete(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("tags_list"))

if __name__ == "__main__":
    app.run(debug=True)
# Edit tag
@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    if flask.request.method == "POST":
        tag_name = flask.request.form.get("name")
        if tag_name:
            tag.name = tag_name
            db.session.commit()
            return flask.redirect(flask.url_for("tags_list"))
    return flask.render_template("tags-edit.html", tag=tag)

# Delete tag
@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    db.session.delete(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("tags_list"))

# List tags
@app.route("/tags", endpoint="tags_list")
def tags_list():
    db = models.db
    tags = db.session.execute(db.select(models.Tag).order_by(models.Tag.name)).scalars()
    return flask.render_template("tags-list.html", tags=tags)

if __name__ == "__main__":
    app.run(debug=True)




# Edit note
@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)
    form = forms.NoteForm(obj=note)
    if form.validate_on_submit():
        form.populate_obj(note)
        note.tags = []
        for tag_name in form.tags.data:
            tag = db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))
    # Prepopulate tags field
    form.tags.data = [tag.name for tag in note.tags]
    return flask.render_template("notes-create.html", form=form, edit=True)

# Delete note
@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)
    db.session.delete(note)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))

# Add tag
@app.route("/tags/add", methods=["GET", "POST"])
def tags_add():
    db = models.db
    if flask.request.method == "POST":
        tag_name = flask.request.form.get("name")
        if tag_name:
            tag = db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
        return flask.redirect(flask.url_for("tags_list"))
    return flask.render_template("tags-add.html")

# Edit tag
@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    if flask.request.method == "POST":
        tag_name = flask.request.form.get("name")
        if tag_name:
            tag.name = tag_name
            db.session.commit()
            return flask.redirect(flask.url_for("tags_list"))
    return flask.render_template("tags-edit.html", tag=tag)

# Delete tag
@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        flask.abort(404)
    db.session.delete(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("tags_list"))

# List tags

# List tags
@app.route("/tags", endpoint="tags_list")
def tags_list():
    db = models.db
    tags = db.session.execute(db.select(models.Tag).order_by(models.Tag.name)).scalars()
    return flask.render_template("tags-list.html", tags=tags)
