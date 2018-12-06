import os
import sys
import json
import pandas as pd
import numpy as np
from uszipcode import SearchEngine
from uszipcode import Zipcode
from datetime import datetime, timedelta
import http.client
import pickle
import seaborn as sns

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

import xgboost as xgb
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import accuracy_score, roc_curve, auc, recall_score



fare_paths = {
    'model': "models/fare_model.pk",
    'sc_object': "models/fare_sc_object.sav"
}


time_paths = {
    'model': "models/time_model.pk",
    'sc_object': "models/time_sc_object.pk"
}

le_paths = {
    'le_pzip': "models/le_pzip.pk",
    'le_dzip': "models/le_dzip.pk",
    'le_py': "models/le_py.pk"
}


features_fare = ['pickup_zipcode', 'dropoff_zipcode',
                 'pickup_day', 'pickup_hour', 'pickup_day_of_week', 'pickup_month',
                 'pickup_year', 'passenger_count', 'trip_distance' , 'trip_time']

features_time = ['pickup_zipcode', 'dropoff_zipcode',
                 'pickup_day', 'pickup_hour', 'pickup_day_of_week', 'pickup_month',
                 'pickup_year', 'passenger_count', 'trip_distance']


api_key = os.environ.get("GOOGLE_MAPS_API_KEY")


def label_encode_columns(df):
    le_pzip = pickle.load(open(le_paths['le_pzip'], "rb"), encoding='latin1')
    df['pickup_zipcode'] = le_pzip.transform(df['pickup_zipcode']) 

    le_dzip = pickle.load(open(le_paths['le_dzip'], "rb"), encoding='latin1')
    df['dropoff_zipcode'] = le_dzip.transform(df['dropoff_zipcode']) 

    le_py = pickle.load(open(le_paths['le_py'], "rb"), encoding='latin1')
    df['pickup_year'] = le_py.transform(df['pickup_year']) 
    
    return df


def get_distance_and_time(pickup, dropoff):
  print("maps.googleapis.com"+"/maps/api/distancematrix/json?units=imperial&origins="+pickup+"&destinations="+dropoff+"&key="+api_key)
  conn = http.client.HTTPSConnection("maps.googleapis.com")
  conn.request("GET", "/maps/api/distancematrix/json?units=imperial&origins="+pickup+"&destinations="+dropoff+"&key="+api_key)
  res = conn.getresponse()
  d = res.read()
  print(d)
  values = {}
  values['trip_time'] = 0
  values['trip_distance'] = 0
  try:
    d = d.decode()
    # print("decode", d)
    d = json.loads(d)
    # print("json", d)
    trip_time = int(d['rows'][0]['elements'][0]['duration']['value'])
    trip_distance = float(d['rows'][0]['elements'][0]['distance']['text'].split(" ")[0])
    # print(d['rows'][0]['elements'][0]['duration']['value'])
    # print(d['rows'][0]['elements'][0]['distance']['text'])
    values['trip_time'] = trip_time
    values['trip_distance'] = trip_distance
    print(values)
    return values
  except Exception as e:
    print(str(e))
    print("\n\n\n\n\n Googlemaps API crashed at input pickup : {} dropoff: {}".format(pickup, dropoff))
    return values


def get_zip_code(latitude,longitude):
    try:
        search = SearchEngine(simple_zipcode=True)
        result = search.by_coordinates(latitude, longitude, radius=5, returns=1)
        return int(result[0].zipcode)
    except Exception as e:
        return 10001


def create_predict_dataframe(pickup_addr_latlong, dropoff_addr_latlong, passenger_count, predict_type):
  pickup_zip = get_zip_code(pickup_addr_latlong[0], pickup_addr_latlong[1])
  dropoff_zip = get_zip_code(dropoff_addr_latlong[0], dropoff_addr_latlong[1])
  pickup = str(pickup_addr_latlong[0])+","+str(pickup_addr_latlong[1])
  dropoff = str(dropoff_addr_latlong[0])+","+str(dropoff_addr_latlong[1])
  curr_time = datetime.now()
  maps_data = get_distance_and_time(pickup,dropoff)
  data = []
  data.append(pickup_zip)
  data.append(dropoff_zip)
  data.append(curr_time.day)
  data.append(curr_time.hour)
  data.append(curr_time.weekday())
  data.append(curr_time.month)
  # data.append(curr_time.year)
  data.append(2014)
  data.append(passenger_count)
  data.append(maps_data['trip_distance'])
  if predict_type == "fare":
    data.append(maps_data['trip_time'])
    print(data)
    df_predict = pd.DataFrame([data], columns=features_fare)
    df_predict = label_encode_columns(df_predict)
    return df_predict 
  else:
    print(data)
    df_predict = pd.DataFrame([data], columns=features_time)
    df_predict = label_encode_columns(df_predict)
    return df_predict 





