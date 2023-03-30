from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os


basedir = os.path.abspath(os.path.dirname(__file__))
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizzalo.db"
app.config["SECRET_KEY"] = "OHSFHSFHojsjdghdg1249673468"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
#patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# this is add by me !!!!!
app.app_context().push()

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
