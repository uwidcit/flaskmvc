from flask import Blueprint, render_template, send_from_directory, jsonify, session
from flask import request, redirect, url_for
from App.models import db, User, Video
from App.controllers import create_user
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask import flash



index_views = Blueprint('index_views', __name__, template_folder='../templates')

class Videos:
    def __init__(self, title, image_url, video_url, description, video_id):
        self.title = title
        self.image_url = image_url
        self.video_url = video_url
        self.description = description
        self.video_id = video_id

def get_video_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def search_by_keyword(api_key, keyword, max_results):
    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        request = youtube.search().list(
            part="id,snippet",
            q=keyword,
            maxResults=max_results
        )
        response = request.execute()
        videos = []
        if "items" in response:
            for item in response["items"]:
                if item["id"].get("kind") == "youtube#video":
                    video_id = item["id"]["videoId"]
                    video_url = get_video_url(video_id)
                    title = item["snippet"]["title"]
                    image = item["snippet"]["thumbnails"]["default"]["url"]
                    description = item["snippet"]["description"]
                    video = Videos(title, image, video_url, description, video_id)
                    videos.append(video)
                else:
                    print("This item is not a video.")
        else:
            print("No videos found.")

    except HttpError as e:
        print("An HTTP error occurred:")
        print(e.content)

    return videos

@index_views.route('/', methods=['GET'])
def index_page():
    videos = search_by_keyword("AIzaSyAa3sah23VK9X4r0hxsC4xHvWTUeLurpv8", "fitness", 30)
    return render_template('index.html', videos=videos)

@index_views.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        videos = search_by_keyword("AIzaSyAa3sah23VK9X4r0hxsC4xHvWTUeLurpv8", keyword, 39)  
    return render_template('index.html', videos=videos)

@index_views.route('/add', methods=['POST'])
@jwt_required()
def add():
    url = request.form.get('url')
    existing_video = Video.query.filter_by(url=url, user_id=get_jwt_identity()).first()
    if existing_video:
        flash("This video is already in your playlist.")
        return redirect(url_for('index_views.index_page'))

    image = request.form.get('image')
    description = request.form.get('description')
    title = request.form.get('title')
    user = get_jwt_identity()
    current_user = User.query.get(user)

    video = Video(title=title, image=image, url=url, description=description, user_id=current_user.id)
    current_user.videos.append(video)
    
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('index_views.index_page'))




@index_views.route('/playlist')
@jwt_required()
def playlist():
    user = get_jwt_identity()
    current_user = User.query.get(user)
    videos = Video.query.filter_by(user_id=current_user.id).all()
    return render_template('playlist.html', videos=videos)



@index_views.route('/delete', methods=['POST', 'DELETE'])
@jwt_required()
def delete():
    user = get_jwt_identity()
    current_user = User.query.get(user)
    video_id = request.form.get('id')
    video = Video.query.filter_by(id=video_id, user_id=current_user.id).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('index_views.playlist'))

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})





