from pets import db
from pets.models.animal import Animal, AnimalKind
from pets.utils.cast import Cast


class Dog(Animal):
    __tablename__ = "dogs"

    id = db.Column(db.Integer, db.ForeignKey('animals.id'), primary_key=True)
    chip = db.Column(db.String(50))
    is_dangerous = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': AnimalKind.Dog
    }

    def __init__(self, params):
        super(Dog, self).__init__(params)
        self.kind = AnimalKind.Dog
        self.update(params)

    def update(self, params):
        super(Dog, self).update(params)
        self.is_dangerous = Cast.to_bool(params.get('dangerous', False))
        self.chip = params.get('chip')
