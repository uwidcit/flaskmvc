from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})