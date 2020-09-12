from flask_sqlalchemy import SQLAlchemy

# db.Init
db = SQLAlchemy()
# should be db = SQLAlchemy(app) but getting app from app.py using init_app(app)
