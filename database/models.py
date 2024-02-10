from database import database
from flask_login import UserMixin
import bcrypt

db = database.db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    status = db.Column(db.Integer, default=1)
    
    @property
    def is_admin(self):
        return self.status == 2

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
class Apartments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    availability = db.Column(db.Boolean, nullable=False)
    night_price = db.Column(db.Float, nullable=False)

    proprio = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='NO ACTION'))
    
class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    starting_date = db.Column(db.DateTime, nullable=False)
    ending_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    apartment = db.Column(db.Integer, db.ForeignKey(Apartments.id, ondelete='NO ACTION'))
    customer = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='NO ACTION'))