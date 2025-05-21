"""
Notifications blueprint for the ZENITHAPPLYAI application.
"""
from flask import Blueprint

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

from . import routes
