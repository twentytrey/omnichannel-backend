git init
python3 -m venv venv
source "./venv/bin/activate"
touch __init__.py .gitignore README.md requirements.txt pronovserver.wsgi routes.py resource.py Procfile config.py
mkdir -p "./ops"
mkdir -p "./static"
mkdir -p "./models"
mkdir -p "./logs"
mkdir -p "./static/datafiles"
mkdir -p "./ops/accesscontrol"
mkdir -p "./ops/members"
mkdir -p "./ops/language"
mkdir -p "./ops/currency"
mkdir -p "./ops/countryandstate"
pip install Flask flask-restful flask-jwt-extended flask-cors psycopg2-binary passlib paystack python-barcode numpy pandas matplotlib scipy Pillow imageio python-dotenv

pip freeze > requirements.txt