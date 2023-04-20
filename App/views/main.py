import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, User, Competition, Team, Member

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('loginPage.html')


@app.route('/login', methods=['POST'])
def loginAction():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        flash('Logged in successfully.')
        login_user(user)
        return redirect('/competitionsPage')
    else:
        flash('Invalid username or password')
        return redirect('/login')


@app.route('/signUp', methods=['GET'])
def signUp():
    return render_template('signUpPage.html')


@app.route('/signUp', methods=['POST'])
def signUpAction():
    data = request.form
    password = data['password']
    confirm_password = data['confirm_password']
    if password != confirm_password:
        flash('Confirm password is incorrect')
        return redirect(url_for('signUp'))

    newuser = User(username=data['username'], email=data['email'], password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        flash('Account Created!')
        return redirect(url_for('competitionsPage'))
    except:
        db.session.rollback()
        flash("username or email already exists")
        return redirect(url_for('signUp'))


@app.route("/competitionsPage", methods=['GET'])
@login_required
def competitionsPage():
    competitions = Competition.query.all()
    return render_template("competitionsPage.html", competitions=competitions)

@app.route("/adminPage/<username>")
def adminPage(username):
    user = User.query.filter_by(username=username).first()
    competitions = user.comps
    return render_template("adminPage.html", username=username, competitions=competitions)


@app.route("/teamViewPage", methods=['GET'])
@login_required
def teamViewPage():
    teams = Team.query.all()
    return render_template("teamViewPage.html", teams=teams)


# we need the corresponding team object to be passed into this page
@app.route("/participantViewPage", methods=['GET'])
@login_required
def participantViewPage():
    participants = Member.query.all()
    return render_template("participantViewPage.html", participants=participants)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
