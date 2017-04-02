from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
import urllib.request as urllib2
from urllib.parse import urljoin
import json

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

# p = Place()
# places = p.query("1600 Amphitheater Parkway Mountain View CA")
class Place(object):
	def meters_to_walking_time(self, meters):
		# 80 meters in one minute walking time
		return int(meters/80)

	def wiki_path(self, slug):
		return urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ','_'))

	def address_to_latlng(self, address):
		g = geocoder.google(address)
		return (g.lat, g.lng)

	def query(self, address):
		lat, lng = self.address_to_latlng(address)
		print (lat, lng)

		query_url='https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
		g=urllib2.urlopen(query_url)
		results=g.read().decode("utf8")
		#print(results)
		g.close()

		data=json.loads(results)
		#print (data)

		places=[]
		for place in data['query']['geosearch']:
			name=place['title']
			meters=place['dist']
			lat=place['lat']
			lng=place['lon']

			wiki_url=self.wiki_path(name)
			walking_time=self.meters_to_walking_time(meters)

			d={
				'name':name,
				'url':wiki_url,
				'time':walking_time,
				'lat':lat,
				'lng':lng
			}

			places.append(d)

		return places