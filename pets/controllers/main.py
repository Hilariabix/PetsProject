from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from pets.controllers.management import Management
from pets.models.animal import Animal, AnimalKind
from pets.models.contacts import Contact
from pets.utils.data_generator import DataGenerator

main = Blueprint("main", __name__)


@main.route("/")
def index():
    dogs_results = Animal.query.filter(Animal.kind == AnimalKind.Dog, Animal.adopted == False).all()
    cats_results = Animal.query.filter(Animal.kind == AnimalKind.Cat, Animal.adopted == False).all()
    dogs = [[dog.profile_image, dog.details, dog.name, dog.id] for dog in dogs_results]
    cats = [[cat.profile_image, cat.details, cat.name, cat.id] for cat in cats_results]
    data = {"dogs": dogs, "cats": cats}
    return render_template("index.html", data=data)


@main.route("/manager")
@login_required
def manager():
    titles = [["Breed", "amount"]]
    dogs = [title for title in titles]
    for dog in Management.get_dogs_count_by_breed():
        dogs.append(list(dog))
    cats = [title for title in titles]
    for cat in Management.get_cats_count_by_breed():
        cats.append(list(cat))
    adopted_dogs = [title for title in titles]
    for dog in Management.get_adopted_dogs_count_by_breed():
        adopted_dogs.append(list(dog))
    adopted_cats = [title for title in titles]
    for cat in Management.get_adopted_cats_count_by_breed():
        adopted_cats.append(list(cat))
    puppies = [title for title in titles]
    for puppy in Management.get_puppies():
        puppies.append(list(puppy))
    kittens = [title for title in titles]
    for kitten in Management.get_kittens():
        kittens.append(list(kitten))
    employees = Management.get_employees_by_employment(True)
    data = {"dogs": dogs, "cats": cats,
            "adopted_dogs": adopted_dogs, "adopted_cats": adopted_cats,
            "puppies": puppies, "kittens": kittens,
            "employees": employees}
    return render_template("manager_page.html", data=data)


@main.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@main.route("/contact", methods=["POST"])
def receive_contact():
    form = request.form
    Contact(form)
    return render_template("contact.html")


@main.route("/contact/<animal_id>", methods=["GET"])
def receive_adoption_request(animal_id):
    dogs_results = Animal.query.filter(Animal.id == animal_id).first()
    data = {'name': dogs_results.name, 'id': animal_id}

    form = request.form
    Contact(form)
    return render_template("contact.html", data=data)


@main.route("/generate")
def generate():
    generator = DataGenerator()
    generator.run()
    return redirect(url_for("main.index"))
