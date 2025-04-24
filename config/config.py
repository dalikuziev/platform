import os

from environs import Env

env = Env()

# Construct the full absolute path to the .env file (parent of config)
env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

# Check if it exists before reading
if not os.path.exists(env_file_path):
    print(f"File not found: {env_file_path}")
    print('.env fayli topilmadi!')
    print('.env.example faylidan nusxa ko\'chirib shablonni o\'zizga moslang.')
    exit(1)

# Load the .env file
env.read_env(env_file_path)

# Use environment variables
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ADMIN_URL = env.str('ADMIN_URL', default='admin/')
SWAGGER_URL = env.str('SWAGGER_URL', default='swagger/')
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
API_V1_URL = env.str('API_V1_URL')