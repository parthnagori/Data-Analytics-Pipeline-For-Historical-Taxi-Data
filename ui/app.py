import os
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from geopy.geocoders import Nominatim
from data_preprocessing import create_predict_dataframe
from models import get_fare, get_time
import http.client
import json

api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

def get_lat_long(address="175 5th Avenue NYC"):
	address = address.replace(' ', '%20')
	conn = http.client.HTTPSConnection("maps.googleapis.com")
	conn.request("GET", "/maps/api/geocode/json?address="+address+"&key="+api_key)
	res = conn.getresponse()
	try:
		data = res.read()
		# print(data)
		data = data.decode()
		# print("\n\n\n decode ------- ", data)
		data = json.loads(data)
		# print("\n\n\n json ------- ", data)
		lat = data['results'][0]['geometry']['location']['lat']
		lon = data['results'][0]['geometry']['location']['lng']
		print("lat - lon ", lat, lon)
		return (lat, lon)
	except Exception as e:
		print(str(e))
		print("\n\n\n\n\n Googlemaps API crashed at address: {}".format(address))
		return (40.7778747802915, -73.97479181970851)

# def get_lat_long(address="175 5th Avenue NYC"):
# 	geolocator = Nominatim(user_agent="Taxi Fare Prediction")
# 	location = geolocator.geocode(address, timeout=None)
# 	print(location.address)
# 	print(location.latitude, location.longitude)
# 	# Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
# 	return (location.latitude, location.longitude)

def run_prediction(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, predict_type):
	if predict_type == "fare":
		print("\nfare\n")
		pred_df = create_predict_dataframe(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, "fare")
		print(pred_df.head())
		fare = get_fare(pred_df)
		print("Running prediction from pickup: {} tp dropoff: {} for {} passengers".format(pickup_addr_latlong, dropoff_addr_latlong, passenger_count))
		return fare
	else:
		print("\nfare\n")
		pred_df = create_predict_dataframe(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, "time")
		print(pred_df.head())
		time = get_time(pred_df)
		time = float(time)/60.0
		return time
	## call
	return 10

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1234567890'
 
class ReusableForm(Form):
	pickup_addr = TextField('Pickup Address:', validators=[validators.required()])
	dropoff_addr = TextField('Dropoff Address:', validators=[validators.required()])
	passenger_count = IntegerField('Passenger Count:', validators=[validators.required()])
 
@app.route("/", methods=['GET', 'POST'])
def run():
	form = ReusableForm(request.form)
 
	print(form.errors)
	if request.method == 'POST':
		pickup_addr=request.form['pickup_addr']
		dropoff_addr = request.form['dropoff_addr']
		passenger_count = request.form['passenger_count']
		predict_type = request.form['options']
		print(pickup_addr, dropoff_addr, passenger_count)

		if form.validate():
			# Save the comment here.
			pickup_addr_latlong = get_lat_long(pickup_addr)
			dropoff_addr_latlong = get_lat_long(dropoff_addr)
			if predict_type == "fare":
				flash("Your fare would be ${}.".format(run_prediction(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, "fare")))
			elif predict_type == "time":
				flash("It would take you {} minutes.".format(run_prediction(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, "time")))
			else:
				flash("Incorrect input, try again.")
		else:
			print(dir(form.errors), form.errors)
			missing_fields = []
			for field in form.errors:
				if field == 'passenger_count':
					missing_fields.append('Passenger Count')

				elif field == 'dropoff_addr':
					missing_fields.append('Dropoff Address')

				elif field == 'pickup_addr':
					missing_fields.append('Pickup Address')

			flash('Error: All the form fields are required. Check fields {}'.format(missing_fields))
 
	return render_template('app.html', form=form)
 
if __name__ == "__main__":
	app.run()