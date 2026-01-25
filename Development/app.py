from flask import Flask, render_template
from flask_login import LoginManager
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
