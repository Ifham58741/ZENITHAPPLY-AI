"""
Billing blueprint for the ZENITHAPPLYAI application.
"""
from flask import Blueprint

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

from . import routes
