from datetime import datetime, timedelta
from sqlalchemy import func
from pets import db
from pets.models.cat import Cat
from pets.models.dog import Dog
from pets.models.animal import Animal
from pets.models.employee import Employee


class Management(object):

    @staticmethod
    def get_dogs_count_by_breed():
        animals = db.session.query(Dog.breed, func.count(Dog.id)).group_by(Dog.breed).all()
        return animals

    @staticmethod
    def get_adopted_dogs_count_by_breed():
        animals = db.session.query(Dog.breed, func.count(Dog.id)).filter(Dog.adopted).group_by(Dog.breed).all()
        return animals

    @staticmethod
    def get_animals_count_by_cage():
        animals = db.session.query(Animal.cage, func.count(Animal.id)).filter(not Animal.adopted).group_by(Animal.cage).all()
        return animals

    @staticmethod
    def get_puppies():
        puppies = db.session.query(Dog.breed, func.count(Dog.id)).filter(Dog.birth_date > datetime.now() - timedelta(days=365)).group_by(Dog.breed).all()
        return puppies

    @staticmethod
    def get_kittens():
        kittens = db.session.query(Cat.breed, func.count(Cat.id)).filter(Cat.birth_date > datetime.now() - timedelta(days=365)).group_by(Dog.breed).all()
        return kittens

    @staticmethod
    def get_cats_count_by_breed():
        animals = db.session.query(Cat.breed, func.count(Cat.id)).group_by(Cat.breed).all()
        return animals

    @staticmethod
    def get_adopted_cats_count_by_breed():
        animals = db.session.query(Cat.breed, func.count(Cat.id)).filter(Cat.adopted).group_by(Cat.breed).all()
        return animals

    @staticmethod
    def get_employees_by_employment(is_employed):
        employees = Employee.query.filter_by(is_employed=is_employed)
        return employees
