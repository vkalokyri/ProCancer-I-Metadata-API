from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from requests.auth import HTTPBasicAuth
import pandas as pd
import ast
import json
import requests

import  molgenis.client
session = molgenis.client.Session("http://localhost/api/")

app = Flask(__name__)
api = Api(app)


def batch_upload_molgenis(entity_name, entity_dict):

    print("Uploading data...")
    session.add_all(entity_name, entity_dict['entities'])


def saveData(file, entity_name):
    extract_data = pd.read_excel(file, sheet_name=entity_name , dtype=str)
    data = extract_data.to_dict(orient='records') # convert dataframe to dictionary
    data_dict = {'entities': data}
    try:
        batch_upload_molgenis('ProCancerI_'+entity_name, data_dict)
        return "Successfully uploaded ProCancerI_"+entity_name+ " data!"
    except Exception as e:
        return e.message, e.args[1].status_code


def authenticateUser(request):   
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        session.login(username, password)
    except Exception as e:
        return str(e)

@app.route("/importData/", methods=["POST"])
def import_data():
    """Upload a file."""
   
    authenticateUser(request)
    
    if 'data_file' in request.files:
        file = request.files['data_file']
        
        patient_return = saveData(file, "Patient")
        series_return = saveData(file, "Series")

        return patient_return+"\n" +series_return, 201
    else:
        return "Error: You haven't specified a 'data_file' argument in your request.", 

    # Return 201 CREATED
    return "", 201



@app.route("/importPatients/", methods=["PUT","POST"])
def import_patient_data():
    """Upload a file."""
    
    authenticateUser(request)

    if 'data_file' in request.files:
        file = request.files['data_file']
        return saveData(file, "Patient")
    else:
        return "Error: You haven't specified a 'data_file' argument in your request.", 400

    return "", 201

@app.route("/importSeries/", methods=["PUT","POST"])
def import_series_data():
    """Upload a file."""

    authenticateUser(request)

    
    if 'data_file' in request.files:
        file = request.files['data_file']
        return saveData(file, "Series")
    else:
        return "Error: You haven't specified a 'data_file' argument in your request.", 400

    return "", 400



@app.route("/getPatients/", methods=["GET"])
def getPatients():
    """Get Patients"""
   
    authenticateUser(request)
    try:
        patients = session.get('ProCancerI_Patient')
    except Exception as e:
        return e.message, e.args[1].status_code

    return jsonify(patients), 200
    


@app.route("/getSeries/", methods=["GET"])
def getSeries():
    """Get Series"""
   
    authenticateUser(request)
    try:
        series = session.get('ProCancerI_Series')
    except Exception as e:
        return e.message, e.args[1].status_code

    return jsonify(series), 200

    

@app.route("/getPatientByID/", methods=["GET"])
def getPatientByID():
    """Get Patients"""
   
    authenticateUser(request)
    try:
        patient = session.get_by_id('ProCancerI_Patient',request.args.get("id"))
    except Exception as e:
        return e.message, e.args[1].status_code

    del patient['_meta']
    return jsonify(patient), 200


@app.route("/getSeriesByID/", methods=["GET"])
def getSeriesByID():
    """Get Series"""
   
    try:
        url = "http://localhost/api/v2/ProCancerI_Series/"+ request.args.get("id")
        username = request.form.get('username')
        password = request.form.get('password')
        r = requests.get(url, auth=HTTPBasicAuth(username, password))   

        if  r.status_code==200:
            series = json.loads(r.text)
            del series['_meta']
            return series, r.status_code     
        else:
            return r.text, r.status_code        
    except Exception as e:
        return str(e), 400 

   
@app.route("/deletePatientList/", methods=["DELETE"])
def deletePatients():
    """Delete Patients"""
   
    authenticateUser(request)  
    session.delete_list("ProCancerI_Patient", request.args.getlist("list"))
     # Return 201 CREATED
    return "", 201

    
@app.route("/deleteSeriesList/", methods=["DELETE"])
def deleteSeries():
    """Delete Series"""
   
    authenticateUser(request)  
    try:
        deleted=session.delete_list("ProCancerI_Series", request.args.getlist("list"))
    except Exception as e:
        return e.message, e.args[1].status_code
     # Return 200 OK
    return deleted.text, deleted.status_code


@app.route("/deleteAllSeries/", methods=["DELETE"])
def deleteAllSeries():
    """Delete All Series"""
    try:
        url = "http://localhost/api/v1/ProCancerI_Series"
        username = request.form.get('username')
        password = request.form.get('password')
        r = requests.delete(url, auth=HTTPBasicAuth(username, password))
        print(r.status_code)
        print(r.text)
        return r.text, r.status_code
    except Exception as e:
        return  e.message, e.args[1].status_code


@app.route("/deleteAllPatients/", methods=["DELETE"])
def deleteAllPatients():
    """Delete All Series"""
   
    try:
        url = "http://localhost/api/v1/ProCancerI_Patient"
        username = request.form.get('username')
        password = request.form.get('password')
        r = requests.delete(url, auth=HTTPBasicAuth(username, password))
        print(r.status_code)
        print(r.text)
        return r.text, r.status_code
    except Exception as e:
        return str(e)


@app.route("/updatePatientByID/", methods=["PUT"])
def updatePatients():
    """Update Patients"""
    
    authenticateUser(request)  

    try:
        updated=session.update_one("ProCancerI_Patient", request.args.get("id"),  request.args.get("attribute"), request.args.get("newValue"))
    except Exception as e:
        return e.message, e.args[1].status_code
     # Return 200 OK
    return updated.text, updated.status_code
  

@app.route("/updateSeriesByID/", methods=["PUT"])
def updateSeries():
    """Update Series"""
    
    authenticateUser(request)  
    try:
        updated=session.update_one("ProCancerI_Series", request.args.get("id"),  request.args.get("attribute"), request.args.get("newValue"))
    except Exception as e:
        return e.message, e.args[1].status_code
     # Return 200 OK
    return updated.text, updated.status_code


if __name__ == '__main__':
    app.run()  # run our Flask app