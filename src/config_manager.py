import yaml
from typing import Dict, Any

class ConfigManager:
    """Manages application configurations across environments"""
    
    def __init__(self):
        self.configs = {}
    
    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
        
        env_name = config.get('environment', 'unknown')
        self.configs[env_name] = config
        return config
    
    def get_config(self, environment: str) -> Dict[str, Any]:
        """Get configuration for specific environment"""
        return self.configs.get(environment, {})
    
    def list_environments(self):
        """List all loaded environments"""
        return list(self.configs.keys())
    
    def compare_configs(self, env1: str, env2: str) -> Dict[str, Any]:
        """Compare configurations between two environments"""
        config1 = self.get_config(env1)
        config2 = self.get_config(env2)
        
        differences = {}
        
        # Compare database settings
        if config1.get('database') != config2.get('database'):
            differences['database'] = {
                env1: config1.get('database'),
                env2: config2.get('database')
            }
        
        # Compare API settings
        if config1.get('api') != config2.get('api'):
            differences['api'] = {
                env1: config1.get('api'),
                env2: config2.get('api')
            }
        
        # Compare features
        if config1.get('features') != config2.get('features'):
            differences['features'] = {
                env1: config1.get('features'),
                env2: config2.get('features')
            }
        
        return differences
    
    def validate_config(self, environment: str) -> bool:
        """Basic validation of configuration"""
        config = self.get_config(environment)
        if not config:
            return False
        
        # Check required sections exist
        required_sections = ['environment', 'database', 'api', 'features']
        if not all(section in config for section in required_sections):
            return False
        
        # Check database has required fields
        db = config.get('database', {})
        required_db_fields = ['host', 'port', 'name']
        if not all(field in db for field in required_db_fields):
            return False
        
        return True
    
    def get_database_host(self, environment: str) -> str:
        """Helper to get database host for environment"""
        config = self.get_config(environment)
        return config.get('database', {}).get('host', '')
    
    def get_api_url(self, environment: str) -> str:
        """Helper to get API URL for environment"""
        config = self.get_config(environment)
        return config.get('api', {}).get('base_url', '')
    
    def is_debug_enabled(self, environment: str) -> bool:
        """Check if debug mode is enabled for environment"""
        config = self.get_config(environment)
        return config.get('features', {}).get('debug_mode', False)

