"""
API blueprint for the ZENITHAPPLYAI web application.
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api import routes, auth, auth_debug, job_configs, resumes, job_applications, job_tasks
