from pets import db
from pets.models.person import Person, Role
from pets.utils.cast import Cast


class Employee(Person):
    __tablename__ = 'employees'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(10), db.ForeignKey('people.id'), primary_key=True)
    salary = db.Column(db.Integer)
    job_percentages = db.Column(db.Integer, default=100)
    bank_account_details = db.Column(db.String(250), nullable=True)
    is_employed = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        'polymorphic_identity': Role.Employee,
    }

    def __init__(self, params):
        super(Employee, self).__init__(params)
        self.update(params)

    def update(self, params):
        super(Employee, self).update(params)
        self.salary = params["salary"]

        job_percentages = int(params["job_percentages"])
        if not (0 <= job_percentages <= 100):
            raise ValueError("Job percentages must be between 0 to 100")
        self.job_percentages = job_percentages

        self.bank_account_details = params.get("bank_account_details")
        self.is_employed = Cast.to_bool(params.get("is_employed"))

    @property
    def is_manager(self):
        return self.role == Role.Manager
