import os
import importlib.util
import sys

def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    config_base_path = './App'

    # Check for custom_config.py file; adjust path as needed
    custom_config_path = os.path.join(config_base_path, 'custom_config.py')
    default_config_path = os.path.join(config_base_path, 'default_config.py')

    if os.path.exists(custom_config_path):
        spec = importlib.util.spec_from_file_location("custom_config", custom_config_path)
    else:
        spec = importlib.util.spec_from_file_location("default_config", default_config_path)

    config_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = config_module
    spec.loader.exec_module(config_module)

    if config['ENV'] == "DEVELOPMENT":
        config['SQLALCHEMY_DATABASE_URI'] = config_module.SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = config_module.SECRET_KEY
        config['JWT_SECRET_KEY'] = config_module.SECRET_KEY
    else:
        config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', config_module.SQLALCHEMY_DATABASE_URI)
        config['SECRET_KEY'] = os.environ.get('SECRET_KEY', config_module.SECRET_KEY)
        config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', config_module.SECRET_KEY)
        config['DEBUG'] = config['ENV'].upper() != 'PRODUCTION'

    # Default configurations that don't depend on the environment
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config['TEMPLATES_AUTO_RELOAD'] = True
    config['PREFERRED_URL_SCHEME'] = 'https'
    config['UPLOADED_PHOTOS_DEST'] = "App/uploads"

    return config

config = load_config()