from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from pets import db
from pets.models.animal import Animal
from pets.models.employee import Employee, Role


class Manager(Employee, UserMixin):
    __tablename__ = 'managers'

    id = db.Column(db.String(10), db.ForeignKey('employees.id'), primary_key=True)
    password = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': Role.Manager,
    }

    def __init__(self, params):
        super(Manager, self).__init__(params)
        self.update(params)
        self.role = Role.Manager

    def update(self, params):
        super(Manager, self).update(params)
        if "password" in params:
            self.set_password(params["password"])

    def fire(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValueError(f"Employee ID {employee_id} was not found")

        employee.is_employed = False
        db.session.commit()
        print(f'{employee.name.title()} ({employee_id}) have been fired')

    def execution(self, animal_id):
        animal = Animal.query.get(animal_id)
        if not animal:
            raise ValueError(f"Animal ID {animal_id} was not found")
        db.session.delete(animal)
        db.session.commit()
        print(f'{animal.id} was executed')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    @staticmethod
    def pay_salary(employee: Employee):
        print(f'Salary have been payed for: {employee.name}')
