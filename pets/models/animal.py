from datetime import datetime
from enum import Enum

from pets import db
from pets.utils.cast import Cast


class AnimalGender(Enum):
    Unspecified = "Unspecified"
    Male = "Male"
    Female = "Female"


class AnimalColor(Enum):
    Unspecified = "Unspecified"
    White = "White"
    Black = "Black"
    Brown = "Brown"
    Gray = "Gray"


class AnimalSize(Enum):
    Small = "Small"
    Medium = "Medium"
    Big = "Big"


class AnimalKind(Enum):
    Dog = "Dog"
    Cat = "Cat"


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.Enum(AnimalGender))
    birth_date = db.Column(db.DateTime, nullable=True)

    kind = db.Column(db.Enum(AnimalKind))

    breed = db.Column(db.String(100))
    size = db.Column(db.Enum(AnimalSize))
    weight = db.Column(db.Float)

    cage = db.Column(db.Integer, nullable=True)

    arrival_date = db.Column(db.DateTime, default=datetime.now())
    date_of_sterilization = db.Column(db.DateTime, nullable=True)

    fruitful = db.Column(db.Boolean, default=True)
    is_trained = db.Column(db.Boolean, default=False)
    friendly = db.Column(db.Boolean, default=True)
    adopted = db.Column(db.Boolean, default=False)
    details = db.Column(db.String(250), nullable=True)

    profile_image = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'animals',
        'polymorphic_on': kind
    }

    def __init__(self, params):
        self.update(params)

    def update(self, params):
        self.name = params['name']
        self.kind = AnimalKind(params['kind'])
        self.gender = AnimalGender(params['gender'])

        self.breed = params['breed']
        self.size = AnimalSize(params['size'])
        self.weight = float(params['weight'])

        self.cage = int(params['cage'])

        self.birth_date = Cast.to_datetime(params.get('birth_date'))
        self.arrival_date = Cast.to_datetime(params.get('arrival_date'))

        self.fruitful = Cast.to_bool(params.get('fruitful'))
        self.is_trained = Cast.to_bool(params.get('is_trained'))
        self.friendly = Cast.to_bool(params.get('friendly'))
        self.adopted = Cast.to_bool(params.get('adopted'))

        self.details = params.get('details')
        if 'profile_image' in params:
            self.profile_image = params['profile_image']
