"""
API routes for job configurations in the ZENITHAPPLYAI web application.
"""
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.api import api_bp
from app.models import User, JobConfig, SubscriptionPlan


@api_bp.route('/job-configs', methods=['GET'])
@jwt_required()
def get_job_configs():
    """Get all job configurations for the current user."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    configs = user.job_configs.all()
    return jsonify({
        'job_configs': [config.to_dict() for config in configs]
    })


@api_bp.route('/job-configs/<int:config_id>', methods=['GET'])
@jwt_required()
def get_job_config(config_id):
    """Get a specific job configuration."""
    user_id = get_jwt_identity()
    config = JobConfig.query.filter_by(id=config_id, user_id=user_id).first_or_404()
    
    return jsonify(config.to_dict())


@api_bp.route('/job-configs', methods=['POST'])
@jwt_required()
def create_job_config():
    """Create a new job configuration."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Check if user has reached the maximum number of job configs
    subscription = user.subscription
    if subscription and subscription.is_active():
        # Get the subscription plan
        plan = SubscriptionPlan.query.filter_by(name=subscription.plan).first()
        if plan and plan.features:
            import json
            try:
                features = json.loads(plan.features)
                max_configs = features.get('max_job_configs')
                
                # Special case for Free Trial plan - limit to 1 job config
                if plan.name == 'Free Trial' and user.job_configs.count() >= 1:
                    return jsonify({
                        'error': 'Free Trial plan is limited to 1 job configuration. Please upgrade your plan to create more.'
                    }), 403
                # For other plans, use the max_configs from features
                elif max_configs and user.job_configs.count() >= int(max_configs):
                    return jsonify({
                        'error': f'You have reached the maximum number of job configurations ({max_configs}) allowed by your subscription plan.'
                    }), 403
            except (json.JSONDecodeError, ValueError) as e:
                current_app.logger.error(f"Error parsing subscription plan features: {e}")
    
    data = request.json
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Job configuration name is required'}), 400
    
    # Create new job config
    config = JobConfig(user_id=user_id)
    
    # Set basic fields
    config.name = data.get('name')
    config.is_default = data.get('is_default', False)
    config.remote = data.get('remote', False)
    config.distance = data.get('distance', 10)
    config.apply_once_at_company = data.get('apply_once_at_company', True)
    
    # Set JSON fields
    if 'experience_levels' in data:
        config.experience_levels = data['experience_levels']
    
    if 'job_types' in data:
        config.job_types = data['job_types']
    
    if 'date_filters' in data:
        config.date_filters = data['date_filters']
    
    if 'searches' in data:
        config.searches = data['searches']
    
    if 'company_blacklist' in data:
        config.company_blacklist = data['company_blacklist']
    
    if 'title_blacklist' in data:
        config.title_blacklist = data['title_blacklist']
    
    if 'job_applicants_threshold' in data:
        config.job_applicants_threshold = data['job_applicants_threshold']
    
    # If this is the default config, unset default flag on other configs
    if config.is_default:
        for other_config in user.job_configs:
            if other_config.is_default:
                other_config.is_default = False
    
    db.session.add(config)
    db.session.commit()
    
    return jsonify(config.to_dict()), 201


@api_bp.route('/job-configs/<int:config_id>', methods=['PUT'])
@jwt_required()
def update_job_config(config_id):
    """Update a job configuration."""
    user_id = get_jwt_identity()
    config = JobConfig.query.filter_by(id=config_id, user_id=user_id).first_or_404()
    
    data = request.json
    
    # Update basic fields
    if 'name' in data:
        config.name = data['name']
    
    if 'is_default' in data:
        config.is_default = data['is_default']
    
    if 'remote' in data:
        config.remote = data['remote']
    
    if 'distance' in data:
        config.distance = data['distance']
    
    if 'apply_once_at_company' in data:
        config.apply_once_at_company = data['apply_once_at_company']
    
    # Update JSON fields
    if 'experience_levels' in data:
        config.experience_levels = data['experience_levels']
    
    if 'job_types' in data:
        config.job_types = data['job_types']
    
    if 'date_filters' in data:
        config.date_filters = data['date_filters']
    
    if 'searches' in data:
        config.searches = data['searches']
    
    if 'company_blacklist' in data:
        config.company_blacklist = data['company_blacklist']
    
    if 'title_blacklist' in data:
        config.title_blacklist = data['title_blacklist']
    
    if 'job_applicants_threshold' in data:
        config.job_applicants_threshold = data['job_applicants_threshold']
    
    # If this is the default config, unset default flag on other configs
    if config.is_default:
        for other_config in JobConfig.query.filter(
            JobConfig.user_id == user_id,
            JobConfig.id != config_id,
            JobConfig.is_default == True
        ).all():
            other_config.is_default = False
    
    db.session.commit()
    
    return jsonify(config.to_dict())


@api_bp.route('/job-configs/<int:config_id>', methods=['DELETE'])
@jwt_required()
def delete_job_config(config_id):
    """Delete a job configuration."""
    user_id = get_jwt_identity()
    config = JobConfig.query.filter_by(id=config_id, user_id=user_id).first_or_404()
    
    db.session.delete(config)
    db.session.commit()
    
    return jsonify({'message': 'Job configuration deleted successfully'})


@api_bp.route('/job-configs/<int:config_id>/set-default', methods=['POST'])
@jwt_required()
def set_default_job_config(config_id):
    """Set a job configuration as the default."""
    user_id = get_jwt_identity()
    config = JobConfig.query.filter_by(id=config_id, user_id=user_id).first_or_404()
    
    # Unset default flag on other configs
    for other_config in JobConfig.query.filter(
        JobConfig.user_id == user_id,
        JobConfig.id != config_id,
        JobConfig.is_default == True
    ).all():
        other_config.is_default = False
    
    config.is_default = True
    db.session.commit()
    
    return jsonify({'message': 'Default job configuration set successfully'})
