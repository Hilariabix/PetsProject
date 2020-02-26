from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from pets import db
from pets.models.animal import Animal, AnimalKind
from pets.models.animal_factory import AnimalFactory
from pets.utils.file_system import FileSystem
animals = Blueprint("animals", __name__)


@animals.route("/animals")
@login_required
def get_all_animals():
    try:
        results = Animal.query.all()
        if not results:
            raise ValueError("No Animals")
    except Exception as ex:
        results = None
        flash("Error: {}".format(ex), "error")
    return render_template("animals/animals.html", animals_list=results)


@animals.route("/animals/<animal_id>", methods=["GET"])
@login_required
def get_animal(animal_id):
    try:
        animal = Animal.query.get(animal_id)
        if not animal:
            raise ValueError("Animal ID {} was not found".format(animal_id))
    except Exception as ex:
        flash("Error: {}".format(ex), "error")
        return redirect(url_for("animals.get_all_animals"))

    return render_template("animals/view.html", animal=animal, method="POST", action="/animals/{}".format(animal_id))


@animals.route("/animals/<animal_id>", methods=["POST"])
@login_required
def update_animal(animal_id):
    try:
        exist_animal = Animal.query.get(animal_id)
        if not exist_animal:
            raise ValueError("Animal ID {} was not found".format(animal_id))

        exist_animal.update(request.form)
        db.session.commit()
        flash("{} was updated successfully".format(exist_animal.name), "info")
    except Exception as ex:
        flash("Error: {}".format(ex), "error")

    return redirect(url_for("animals.get_all_animals"))


@animals.route("/animals/add", methods=["GET"])
@login_required
def add_animal_view():
    return render_template("animals/view.html", method="POST", action="/animals/add", animal=None)


@animals.route("/animals/add", methods=["POST"])
@login_required
def add_animal():
    try:
        animal_kind = AnimalKind(request.form.get("kind"))
        new_animal = AnimalFactory.create(animal_kind, request.form)

        profile_image = FileSystem.upload_photo_from_request(request, "photo", "adoption")
        if profile_image:
            new_animal.profile_image = profile_image

        db.session.add(new_animal)
        db.session.commit()
        flash("{} was added successfully".format(new_animal.name), "info")
    except Exception as ex:
        flash("Error: Failed to add an animal, {}".format(ex), "error")

    return redirect(url_for("animals.get_all_animals"))


@animals.route("/animals/delete/<animal_id>", methods=["GET"])
@login_required
def delete_animal(animal_id):
    try:
        exist_animal = Animal.query.get(animal_id)
        if not exist_animal:
            raise ValueError("Animal ID {} was not found".format(animal_id))

        db.session.delete(exist_animal)
        db.session.commit()
        flash("{} was deleted successfully".format(exist_animal.name), "info")
    except Exception as ex:
        flash("Error: {}".format(ex), "error")

    return redirect(url_for("animals.get_all_animals"))
