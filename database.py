from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(120))
    reason_of_contact = db.Column(db.String(100))
    urgency = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'reason_of_contact': self.reason_of_contact,
            'urgency': self.urgency,
            'timestamp': self.timestamp.isoformat()
        }
