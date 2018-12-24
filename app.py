# Name: app.py
# Purpose: Flask App Python File
# Author: David Wasserman
# Last Modified: 12/16/2018
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
import sys, os, json
import pandas as pd
from flask import Flask, render_template, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

# Paths
file_dir = os.path.dirname(os.path.realpath('__file__'))
static_dir = os.path.join(file_dir, "static")
application_dir = os.path.join(static_dir, "application")
data_dir = os.path.join(application_dir, "data")
gjson = os.path.join(data_dir, "WestValleyATPNetwork.geojson")
# Variables

fields = ["PedConnect_Score", "LSBikConnect_Score", "Strava_Score", "UCATWKUse_Score", "UCATBKUse_Score",
          "Bike_Ln_Score", "Crss_WK_Score", "SidWlk_Score", "Safety_Score"]
weight_names = ["ped-connectivity", "bike-connectivity", "strava", "ucats-walk", "ucats-bike",
          "bike-lane", "crosswalk", "sidewalk", "safety"]
weights = [.1,.1,.0375,.125,.0875,.1,.1,.1,.25]
out_field = "Priority_Score"
# Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


# Functions

def get_df_from_geojson_properties(geojson_path):
    """Returns geojson properties as a dataframe
    :param - geojson_path - path to geojson data
    :returns - dataframe - dataframe of geojson properties"""
    with open(gjson) as file:
        data = json.load(file)
        records = []
        for feature in data["features"]:
            dict = feature["properties"]
            records.append((dict))
        df = pd.DataFrame(records)
        return df


def weighted_sum(df, value_columns, weights, new_output_column="WeightedSum"):
    """Description:
    Take passed dataframe and add a column with the weighted output of value columns and their weights.
     Number of weights must match the number of value columns passed
     :param df - dataframe
     :param value_columns - list of column names in df to sum
     :param weights - list of weights in same order as appropriate column
     :param new_output_column - string of new column name added to df
     :return df with new output column added to it"""
    assert len(value_columns) == len(weights), "length of value columns and length of weights don't match"
    data = df[value_columns].copy()
    weight_df = pd.DataFrame(weights, index=value_columns, columns=[0])
    df[new_output_column] = data.dot(weight_df)
    return df


# App
@app.route("/")
def index():
    """
    Main App Route
    :param None
    :return render template - html base
    """
    return render_template("index.html")


@app.route("/network_geojson")
def reweighted_geojson():
    """
    Returns reweighted geojson data to app.
    :param: None
    :return geojson - network data edited
    """
    df = get_df_from_geojson_properties(gjson)
    df = df[fields]
    df = weighted_sum(df, fields, weights, out_field)
    df= get_weights
    return render_template("render_data.html",weighted_df = df.to_html())

@app.route('/', methods=['POST'])
def get_weights(weight_fields):
    """Given a list of html id names, return the values of the input forms as a dictionary
    @:param weight_fields - list of strings of names
    @:return weight_dictionary - dictionary of string names and their weights"""
    weight_dictionary={}
    for weight_id in weight_fields:
        weight = request.form[weight_id]
        weight_dictionary[weight_id]=weight
    return weight_dictionary

if __name__ == '__main__':
    # get_df_from_geojson_properties(gjson)
    app.run(debug=True)
