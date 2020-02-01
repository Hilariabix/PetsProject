from pets import db
from pets.models.animal import Animal, AnimalKind
from pets.utils.cast import Cast


class Cat(Animal):
    __tablename__ = "cats"

    id = db.Column(db.Integer, db.ForeignKey('animals.id'), primary_key=True)
    is_playful = db.Column(db.Boolean, default=False)
    is_hairy = db.Column(db.Boolean, default=False)
    is_loudly = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': AnimalKind.Cat
    }

    def __init__(self, params):
        super(Cat, self).__init__(params)
        self.kind = AnimalKind.Cat
        self.update(params)

    def update(self, params):
        super(Cat, self).update(params)
        self.is_playful = Cast.to_bool(params.get('is_playful', False))
        self.is_hairy = Cast.to_bool(params.get('is_hairy', False))
        self.is_loudly = Cast.to_bool(params.get('is_loudly', False))
