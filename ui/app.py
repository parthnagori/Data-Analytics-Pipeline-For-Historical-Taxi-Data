from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from geopy.geocoders import Nominatim

def get_lat_long(address="175 5th Avenue NYC"):
	geolocator = Nominatim(user_agent="Taxi Fare Prediction")
	location = geolocator.geocode(address)
	print(location.address)
	print(location.latitude, location.longitude)
	# Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
	return (location.latitude, location.longitude)

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
 
	print form.errors
	if request.method == 'POST':
		pickup_addr=request.form['pickup_addr']
		dropoff_addr = request.form['dropoff_addr']
		passenger_count = request.form['passenger_count']
		print pickup_addr, dropoff_addr, passenger_count

		if form.validate():
			# Save the comment here.
			pickup_addr_latlong = get_lat_long(pickup_addr)
			dropoff_addr_latlong = get_lat_long(dropoff_addr)
			flash("")
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