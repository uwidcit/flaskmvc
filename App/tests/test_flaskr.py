import os, tempfile, pytest, logging
from App.main import create_app
from App.database import init_db

from App.controllers import ( 
    get_all_users_json,
    create_user
)

# https://stackoverflow.com/questions/4673373/logging-within-pytest-testshttps://stackoverflow.com/questions/4673373/logging-within-pytest-tests

LOGGER = logging.getLogger(__name__)


# fixetures are used to setup state in the app before the test
# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

'''
   Unit Tests
'''

# This is a unit test because there are no side effects
# Test 1: Checks if api/lol route returns 'lol'
def test_hello(empty_db):
    response = empty_db.get('/api/lol')
    assert b'lol' in response.data