from pets import db
from pets.models.animal import Animal
from pets.models.employee import Employee
from pets.models.person import Person
from pets.utils.cast import Cast


class DataUtils(object):

    @staticmethod
    def set_info(model, info):
        if not isinstance(model, db.Model):
            raise ValueError("Can set_info only to db.Model objects")

        columns = list(model.__table__.columns)
        if isinstance(model, Animal):
            columns.extend(list(Animal.__table__.columns))
        if isinstance(model, Person):
            columns.extend(list(Person.__table__.columns))
        if isinstance(model, Employee):
            columns.extend(list(Employee.__table__.columns))

        for col in columns:
            if col.name in info:
                # all the values appear in request as string
                # cast each value to the right type according to the col type
                val = Cast.cast_to_col(info[col.name], col)
                setattr(model, col.name, val)
