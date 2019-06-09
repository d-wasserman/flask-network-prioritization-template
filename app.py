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
from flask import Flask, render_template, jsonify,session
from flask import request
from flask import redirect,url_for

# Config
app = Flask(__name__)
app.secret_key = os.urandom(24) # Random Key Generated for Sessions

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

def get_df_from_geojson_obj(geojson_obj):
    """Returns geojson dict-like object properties as a dataframe
    :param - geojson_obj - dict-like data object from json load
    :returns - dataframe - dataframe of geojson properties"""
    records = []
    for feature in geojson_obj["features"]:
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

def return_edited_geojson(gjson_data,dataframe):
    """This function will return a geojson data with properties edited based on a passed property name, and
    and ordered list of values.
    :param gjson_data- open data file from json load - dict-like
    :param dataframe - pd.dataframe with column names to replace in the geojson and values replace in feature order
    :returns data - edited dictionary
    """
    for property in dataframe.columns:
        values = dataframe[property].tolist()
        for idx,feature in enumerate(gjson_data["features"]): # Pass by reference
            dict = feature["properties"]
            dict[property] = values[idx]
    return gjson_data

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
    if "dict" not in session:
        # Default Variables [Change as needed]
        fields = ["PedConnect_Score", "LSBikConnect_Score", "Strava_Score", "UCATWKUse_Score", "UCATBKUse_Score",
                  "Bike_Ln_Score", "Crss_WK_Score", "SidWlk_Score", "Safety_Score"]
        weight_names = ["pedconnectivity", "bikeconnectivity", "strava", "ucatsped", "ucatsbicycle",
                        "bikelane", "crosswalk", "sidewalk", "safety"]  # same order as weight fields
        weights = [10.0, 10.0, 3.75, 12.5, 8.75, 10.0, 10.0, 10.0, 25.0]  # must be in same order as weight_names
        weight_dictionary = {i: j for i, j in zip(weight_names, weights)}
        out_field = "Priority_Score"
        old_out_field = "Last_Priority_Score"
        score_difference = "Difference_Score"
        session["weights"] = weights
        session["last_weights"] = weights
        session["weight_names"] = weight_names
        session["fields"] = fields
        session["new_column"] = out_field
        session["old_column"] = old_out_field
        session["diff_column"] = score_difference
        session["dict"] = weight_dictionary

    else:
        weight_dictionary = session["dict"]

    return render_template("index.html",**weight_dictionary)


@app.route("/api/network_geojson.geojson")
def reweighted_geojson():
    """
    Returns reweighted geojson data to app.
    :param: None
    :return geojson - network data edited
    """
    with open(base_gjson) as file:
        data = json.load(file)
    df = get_df_from_geojson_obj(data)
    df = df[session["fields"]]
    df = weighted_sum(df, session["fields"], session["last_weights"], session["old_column"])
    df = weighted_sum(df, session["fields"], session["weights"], session["new_column"])
    df[session["diff_column"]] = df[session["new_column"]]- df[session["old_column"]]
    data = return_edited_geojson(data,df[[session["old_column"],session["new_column"],session["diff_column"]]].copy())
    geojson_service = jsonify(data)
    session["last_weights"] = session["weights"]
    return geojson_service

@app.route("/revise_weights",methods=["GET","POST"])
def revise_weights():
    """
    Returns reweighted geojson data to app.
    :param: None
    :return weights
    """
    if request.method == 'POST':
        weight_list = get_weights(session["weight_names"])
    else:
        weight_list = session["weights"]
    session["weights"] = weight_list
    session["dict"] = {i:j for i,j in zip(session["weight_names"],session["weights"])}
    return jsonify(session["dict"])




if __name__ == '__main__':
    app.run(debug=True)
