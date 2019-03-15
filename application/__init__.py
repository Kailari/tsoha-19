from flask import Flask
import application.settings
app = Flask(__name__)


settings.load_env()

bcrypt = settings.configure_bcrypt(app)
db = settings.configure_database(app)

settings.load_models()
settings.load_views()

settings.configure_login_manager(app)
settings.create_context_processors(app)

try:
    db.create_all()
except:
    pass

try:
    from application.auth.models import create_account_triggers
    create_account_triggers()
except:
    pass
