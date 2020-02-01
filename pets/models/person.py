from datetime import date
from enum import Enum

from pets import db
from pets.utils.cast import Cast


class Gender(Enum):
    Male = 'Male'
    Female = 'Female'


class Role(Enum):
    Adopter = 'Adopter'
    Employee = 'Employee'
    Manager = 'Manager'


class Person(db.Model):
    __tablename__ = "people"

    id = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.Enum(Gender, name="person_gender"))
    role = db.Column(db.Enum(Role))
    birth_date = db.Column(db.DateTime, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'people',
        'polymorphic_on': role
    }

    def __init__(self, params):
        self.update(params)

    def update(self, params):
        self.id = params["id"]
        self.name = params["name"]
        self.gender = Gender(params["gender"])
        self.role = Role(params["role"])

        self.birth_date = Cast.to_datetime(params.get("birth_date"))
        self.phone_number = params.get("phone_number")
        email = params.get("email")
        self.email = email.lower() if email else None

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
