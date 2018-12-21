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
import sys,os
import pandas as pd
from pandas.io.json import json_normalize
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
#paths
file_dir  = os.path.dirname(os.path.realpath('__file__'))
static_dir = os.path.join(file_dir,"static")
application_dir = os.path.join(static_dir,"application")
data_dir = os.path.join(application_dir,"data")
gjson = os.path.join(data_dir,"WestValleyATPNetwork.geojson")
print(gjson)
# print(json_normalize(gjson,"properties"))

# Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
# Functions
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
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
