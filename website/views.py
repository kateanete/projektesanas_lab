from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Food
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    search_food = None
    if request.method == "POST":
        note = request.form.get("note")  # Gets the note from the HTML
        search = request.form.get("search")  # Gets the search query from the HTML

        if search:  # If there's a search query
            search_food = Food.query.filter(Food.product.like(f"%{search}%")).all()
            # This will find all Food instances where the product name contains the search query

        elif len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(
                data=note, user_id=current_user.id
            )  # providing the schema for the note
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user, search_food=search_food)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(
        request.data
    )  # this function expects a JSON from the INDEX.js file
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
