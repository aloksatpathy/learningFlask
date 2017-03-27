from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__='Users'
	uID = db.Column(db.Integer, primary_key = True)
	firstName = db.Column(db.String(100))
	lastName = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True)
	pwdHash = db.Column(db.String(54))

	def __init__(self, firstName, lastName, email, password):
		self.firstName = firstName.title()
		self.lastName = lastName.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdHash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdHash, password)