from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from geopy.geocoders import Nominatim

def get_lat_long(address="175 5th Avenue NYC"):
	geolocator = Nominatim(user_agent="Taxi Fare Prediction")
	location = geolocator.geocode(address)
	print(location.address)
	# Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
	print((location.latitude, location.longitude))
	print(location.raw)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1234567890'
 
class ReusableForm(Form):
    pickup_addr = TextField('Pickup Address:', validators=[validators.required()])
    dropoff_addr = TextField('Dropoff Address:', validators=[validators.required()])
    passenger_count = TextField('Passenger Count:', validators=[validators.required()])
 	
    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)
 
@app.route("/", methods=['GET', 'POST'])
def run():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        pickup_addr=request.form['Pickup Address']
        dropoff_addr = request.form['Dropoff Address']
    	passenger_count = request.form['Passenger Count']
        # print pickup_addr, dropoff_addr, passenger_count
 
        if form.validate():
            # Save the comment here.
            flash("inputs {} {} {}".format(pickup_addr, dropoff_addr, passenger_count))
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('app.html', form=form)
 
if __name__ == "__main__":
    app.run()