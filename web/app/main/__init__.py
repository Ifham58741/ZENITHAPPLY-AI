"""
Main blueprint for the ZENITHAPPLYAI web application.
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.main import routes
