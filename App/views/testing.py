from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
import os
from dotenv import load_dotenv
import json
import http.client

testing_views= Blueprint('testing_views', __name__, template_folder='../templates')

load_dotenv()
api_key=os.getenv("API_KEY")

def fetch_data(param):
    conn = http.client.HTTPSConnection("work-out-api1.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "work-out-api1.p.rapidapi.com"
}

    conn.request("GET", f"/search?Muscles={param}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"))
    return data.decode('utf-8')

@testing_views.route('/testing', methods=['GET'])
def testing_page():
    app_data = fetch_data("biceps")
    app_data=json.loads(app_data)
    print (len(app_data))
    first=app_data[1]
    muscle=first.get('WorkOut')
    return render_template('testing.html', api_data=muscle)

