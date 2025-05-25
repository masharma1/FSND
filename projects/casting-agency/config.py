import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
database_name = os.getenv('DATABASE_NAME', 'casting_agency')
database_path = os.getenv('DATABASE_URL', f'postgresql://postgres:password@localhost:5432/{database_name}')

# Fix for Heroku PostgreSQL URL (if necessary)
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

# Auth0 configuration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-vaa4tqxczeu26tio.us.auth0.com')
API_AUDIENCE = os.getenv('API_AUDIENCE', 'casting-agency-api')
CLIENT_ID = os.getenv('CLIENT_ID', 'JYmMAdwbqYZZWfe6bh7eKtPFqqefm5YL')
ALGORITHMS = ['RS256']

# Flask configuration
DEBUG = os.getenv('DEBUG', 'True') == 'True'