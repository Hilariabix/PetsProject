from enum import Enum
from datetime import datetime
from pets import db
from sqlalchemy.dialects.postgresql import ENUM

from pets.utils.data_utils import DataUtils


class ContactType(Enum):
    ADOPT = 'adopt'
    VOLUNTEER = 'volunteer'
    DONATE = 'donate'
    GOOD = 'goodword'
    COMPLAINTS = 'complaints'


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_date = db.Column(db.DateTime, default=datetime.now())
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    mail = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    subject = db.Column(db.String(250))
    contact_type = db.Column(ENUM(ContactType))

    def __init__(self, content):
        DataUtils.set_info(self, content)
