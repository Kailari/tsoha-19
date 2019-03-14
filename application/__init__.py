from flask import Flask
import application.settings
app = Flask(__name__)


settings.load_env()

bcrypt = settings.configure_bcrypt(app)
db = settings.configure_database(app)

settings.load_models()
settings.load_views()

settings.configure_login_manager()

try:
    db.create_all()

    from application.auth.models import create_account_triggers
    create_account_triggers()
except:
    pass
