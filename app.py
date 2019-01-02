# Name: app.py
# Purpose: Flask App Python File
# Author: David Wasserman
# Last Modified: 12/26/2018
# Copyright: David Wasserman
# Python Version:   3.6
# --------------------------------
# Copyright 2018 David J. Wasserman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------
# Library Import
import os, json
import pandas as pd
from flask import Flask, render_template, jsonify
from flask import request
from flask import redirect,url_for

# Config
app = Flask(__name__)

### DB Config - not used
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# Paths
file_dir = os.path.dirname(os.path.realpath('__file__'))
static_dir = os.path.join(file_dir, "static")
application_dir = os.path.join(static_dir, "application")
data_dir = os.path.join(application_dir, "data")
base_gjson = os.path.join(data_dir, "WestValleyATPNetwork.geojson")
# Variables

fields = ["PedConnect_Score", "LSBikConnect_Score", "Strava_Score", "UCATWKUse_Score", "UCATBKUse_Score",
          "Bike_Ln_Score", "Crss_WK_Score", "SidWlk_Score", "Safety_Score"]
weight_names = ["pedconnectivity", "bikeconnectivity", "strava", "ucatsped", "ucatsbicycle",
          "bikelane", "crosswalk", "sidewalk", "safety"] # same order as weights
weights = [10.0,10.0,3.75,12.5,8.75,10.0,10.0,10.0,25.0] # must be in same order as weight_names
weight_dictionary = {i:j for i,j in zip(weight_names,weights)}
out_field = "Priority_Score"
# Functions

def get_df_from_geojson_properties(geojson_path):
    """Returns geojson properties as a dataframe
    :param - geojson_path - path to geojson data
    :returns - dataframe - dataframe of geojson properties"""
    with open(geojson_path) as file:
        data = json.load(file)
        records = []
        for feature in data["features"]:
            dict = feature["properties"]
            records.append((dict))
        df = pd.DataFrame(records)
        return df


def weighted_sum(df, value_columns, weights, new_output_column="WeightedSum",sum_to_one=True):
    """Description:
    Take passed dataframe and add a column with the weighted output of value columns and their weights.
     Number of weights must match the number of value columns passed
     :param df - dataframe
     :param value_columns - list of column names in df to sum
     :param weights - list of weights in same order as appropriate column
     :param new_output_column - string of new column name added to df
     :param sum_to_one - forces the weights to sum to one
     :return df with new output column added to it"""
    assert len(value_columns) == len(weights), "length of value columns and length of weights don't match"
    if sum_to_one:
        sum_weights = sum(weights)
        weights = [float(i/sum_weights) for i in weights]
    data = df[value_columns].copy()
    weight_df = pd.DataFrame(weights, index=value_columns, columns=[0])
    df[new_output_column] = data.dot(weight_df)
    return df

def return_edited_geojson(gjson_path,property,values):
    """This function will return a geojson data with properties edited based on a passed property name, and
    and ordered list of values.
    :param gjson_path - path to input
    :param property - name of property to replace
    :param values - list of values to replace for property- order in feature order
    :returns data - edited dictionary
    """
    with open(gjson_path) as file:
        data = json.load(file)
        for idx,feature in enumerate(data["features"]): # Pass by reference
            dict = feature["properties"]
            dict[property] = values[idx]
    return data

def get_weights(weight_names):
    """Given a list of html id names, return the values of the input forms as a list in the
    same order as weight names
    @:param weight_fields - list of strings of names
    @:return weight_dictionary - dictionary of string names and their weights"""
    weight_list = []
    for weight_id in weight_names:
        weight = float(request.form[weight_id])
        weight_list.append(weight)
    return weight_list

# App
@app.route("/")
def index():
    """
    Main App Route
    :param None
    :return render template - html base
    """
    return render_template("index.html",**weight_dictionary)


@app.route("/api/network_geojson.geojson")
def reweighted_geojson():
    """
    Returns reweighted geojson data to app.
    :param: None
    :return geojson - network data edited
    """
    df = get_df_from_geojson_properties(base_gjson)
    df = df[fields]
    df = weighted_sum(df, fields, weights, out_field)
    data = return_edited_geojson(base_gjson,out_field,df[out_field].tolist())
    return jsonify(data)

@app.route("/revised_weights",methods=["GET","POST"])
def revised_weights():
    """
    Returns reweighted geojson data to app.
    :param: None
    :return weights
    """
    global weights
    global weight_dictionary
    if request.method == 'POST':
        weight_list = get_weights(weight_names)
    else:
        weight_list = weights
    weights = weight_list
    weight_dictionary = {i:j for i,j in zip(weight_names,weights)}
    return redirect(url_for('index',**weight_dictionary))




if __name__ == '__main__':
    app.run()
