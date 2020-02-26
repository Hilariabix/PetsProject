from pets.models.animal import AnimalKind
from pets.models.cat import Cat
from pets.models.dog import Dog


class AnimalFactory(object):

    @staticmethod
    def create(animal_kind, params):
        if animal_kind == AnimalKind.Dog:
            return Dog(params)
        elif animal_kind == AnimalKind.Cat:
            return Cat(params)
        else:
            raise ValueError(f"Unknown animal kind: {animal_kind}")