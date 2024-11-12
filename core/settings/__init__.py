from pathlib import Path
import os

from dotenv import load_dotenv

#TODO: settings files need to be cleaner
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


app_env = os.environ.get("APP_ENV", None)

if app_env == "PRODUCTION":
    from .production import *
elif app_env == "STAGING":
    from .staging import *
elif app_env == "DEVELOPMENT":
    from .development import *
else:
    from .local import *
