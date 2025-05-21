"""
Authentication blueprint for the ZENITHAPPLYAI web application.
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import routes
