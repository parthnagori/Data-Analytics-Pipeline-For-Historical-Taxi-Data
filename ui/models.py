import os
import random
import pickle
import numpy as np
import pandas as pd
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
    'sc_object': "models/time_sc_object.sav"
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


def get_fare(input_df):
  model = pickle.load(open(fare_paths['model'], "rb"), encoding='latin1')
  sc_object = pickle.load(open(fare_paths['sc_object'], "rb"), encoding='latin1')
  
  # scaled_df = sc_object.transform(input_df)
  temp = sc_object.transform(input_df[features_fare])
  print(temp)
  input_df[features_fare] = temp
  scaled_df = input_df
  print(scaled_df.head())
  predictions = model.predict(scaled_df)
  predictions = predictions.astype(int)
  if predictions:
    return predictions[0]
  else:
    return 0


def get_time(input_df):
  model = pickle.load(open(time_paths['model'], "rb"), encoding='latin1')
  sc_object = pickle.load(open(time_paths['sc_object'], "rb"), encoding='latin1')
  
  # scaled_df = sc_object.transform(input_df)
  temp = sc_object.transform(input_df[features_time])
  print(temp)
  input_df[features_time] = temp
  scaled_df = input_df
  print(scaled_df.head())

  predictions = model.predict(scaled_df)
  predictions = predictions.astype(int)
  if predictions:
    return predictions[0]
  else:
    return 0



