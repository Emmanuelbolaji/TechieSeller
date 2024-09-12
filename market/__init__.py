from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Add this import to handle database migrations


app = Flask(__name__)


# Configuring the SQLite database for the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' # Database instance using SQLAlchemy
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d' # Enables database migrations using Flask-Migrate


# Initializing extensions
db = SQLAlchemy(app) # Database instance using SQLAlchemy
migrate = Migrate(app, db)  # Enables database migrations using Flask-Migrate
bcrypt = Bcrypt(app) # Bcrypt for hashing passwords
login_manager = LoginManager(app) # Manages user sessions and login
login_manager.login_view = "login_page" # Specifies the view for login
login_manager.login_message_category = "info" # Sets the category for login messages


from market import routes  # Import routes after app and extensions are initialized
