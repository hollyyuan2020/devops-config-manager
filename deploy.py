#!/usr/bin/env python3
"""Environment deployment manager"""

import sys
import yaml
from src.config_manager import ConfigManager

def load_deployment_config(environment):
    """Load deployment configuration for environment"""
    config_path = f"configs/{environment}/deployment.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Deployment config not found: {config_path}")
        return None

def deploy_to_environment(environment):
    """Deploy application to specified environment"""
    # Environment mapping
    env_map = {'dev': 'development', 'staging': 'staging', 'prod': 'production'}
    
    if environment not in env_map:
        print(f"Invalid environment: {environment}")
        print("Valid environments: dev, staging, prod")
        return False
    
    full_env_name = env_map[environment]
    
    # Load application config
    manager = ConfigManager()
    app_config_path = f"data/{environment}_config.yaml"
    
    try:
        app_config = manager.load_config(app_config_path)
    except FileNotFoundError:
        print(f"Application config not found: {app_config_path}")
        return False
    
    # Load deployment config
    deploy_config = load_deployment_config(environment)
    if not deploy_config:
        return False
    
    # Validate application config
    if not manager.validate_config(full_env_name):
        print(f"Invalid application configuration for {full_env_name}")
        return False
    
    # Display deployment plan
    print(f"\nDeployment Plan for {environment.upper()}")
    print("=" * 40)
    
    print(f"Environment: {full_env_name}")
    print(f"Database Host: {manager.get_database_host(full_env_name)}")
    print(f"API URL: {manager.get_api_url(full_env_name)}")
    print(f"Debug Mode: {manager.is_debug_enabled(full_env_name)}")
    
    deployment = deploy_config['deployment']
    print(f"Replicas: {deployment['replicas']}")
    print(f"CPU: {deployment['resources']['cpu']}")
    print(f"Memory: {deployment['resources']['memory']}")
    print(f"Image Tag: {deployment['image_tag']}")
    
    # Security check
    db_config = app_config.get('database', {})
    if full_env_name != 'development' and not db_config.get('ssl', False):
        print("\nWARNING: SSL not enabled for non-development environment!")
        return False
    
    print(f"\n✓ {environment} deployment configuration is ready!")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 deploy.py <environment>")
        print("Environments: dev, staging, prod")
        sys.exit(1)
    
    environment = sys.argv[1]
    success = deploy_to_environment(environment)
    
    if not success:
        print(f"\n✗ {environment} deployment failed")
        sys.exit(1)
