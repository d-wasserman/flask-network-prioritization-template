# flask-network-prioritization-template

A sample application using flask and leafet to enable dynamic changes to weights for an arbitrary multicriteria analysis. Inspired by Ian McHargs work on overlay analysis as a method of managing complexity and reflecting human values in planning for human settlement. 

# Summary

This sample project uses sample data from a priorization analysis for West Valley, Utah's Active Transportation Plan to provide an example of how to use flask for dynamically reweighting a multicriteria analysis.

Part of the motivation for this project is to start 2019 by celebrating the 50th aniversary of [Sir Ian McHarg's book "Design With Nature"](https://en.wikipedia.org/wiki/Ian_McHarg). This type of analytical implementation provides a template for open source McHargian style analysis to help planners design with data. 

# Demonstration Animation

![alt text](../main/static/application/assets/Template_Screenshot.gif "Network Prioritization Example")

# Build Information

The dependencies and frameworks used in this template are listed below. 

## Frontend

This template uses the following CSS/JS libraries/frameworks for the frontend. 

* Bootstrap 4.0.0 (Via CDN)

* leaflet 1.7.1

* chroma-js 2.0.2

* jquery 3.6.0

* leaflet-ajax 2.1.0

* lie 3.0.1

* grunt >1.5.3

## Backend

The backend environment uses [Flask](http://flask.pocoo.org/) for app deployment. The python environment used is set up via conda (or pip) using Python version 3.6. The dependencies are listed below. 

* certifi=2018.11.29=py36_1000
* click=7.0=py_0
* flask=1.0.2=py_2
* flask-sqlalchemy=2.3.2=py_0
* itsdangerous=1.1.0=py_0
* jinja2=2.10=py_1
* markupsafe=1.1.0=py36hfa6e2cd_1000
* pandas=0.23.4=py36h830ac7b_1000
* pip=18.1=py36_1000
* python=3.6.6=he025d50_0
* python-dateutil=2.7.5=py_0
* pytz=2018.7=py_0
* setuptools=40.6.3=py36_0
* six=1.12.0=py36_1000
* sqlalchemy=1.2.15=py36hfa6e2cd_1000
* vc=14=0
* vs2015_runtime=14.0.25420=0
* werkzeug=3.1.4=py_0
* wheel=0.32.3=py36_0
* wincertstore=0.2=py36_1002
* blas=1.0=mkl
* mkl=2017.0.3=0
* numpy=1.13.1=py36_0


