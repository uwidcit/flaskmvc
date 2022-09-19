import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import app
from App.database import create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json
)

LOGGER = logging.getLogger(__name__)


#Base fixture all fixtures should inherit from
@pytest.fixture()
def app_fixture():
    app.config.update({"TESTING": True})
    yield app

# Simple fixture for a flask app
@pytest.fixture()
def client(app_fixture):
    return app.test_client()



'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

class UserIntegrationTests(unittest.TestCase):

    # This fixture creates an empty database for the test and deletes it after the test
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')

    def test_create_user(self):
        user = create_user("bob", "bobpass")
        assert user.username == "bob"
    
    def test_get_all_users_json(self):
        create_user("rick", "rickpass")
        users_json = get_all_users_json()
        self.assertListEqual([{"id": 1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)
    