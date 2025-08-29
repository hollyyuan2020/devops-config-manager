import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config_manager import ConfigManager

def test_load_configurations():
    """Test loading configurations from all environments"""
    manager = ConfigManager()
    
    # Load all configurations
    manager.load_config('data/dev_config.yaml')
    manager.load_config('data/staging_config.yaml')
    manager.load_config('data/prod_config.yaml')
    
    # Verify all loaded
    environments = manager.list_environments()
    assert 'development' in environments
    assert 'staging' in environments
    assert 'production' in environments
    
    print("Configuration loading test passed")

def test_environment_differences():
    """Test that different environments have different settings"""
    manager = ConfigManager()
    manager.load_config('data/dev_config.yaml')
    manager.load_config('data/prod_config.yaml')
    
    # Development should have debug enabled
    assert manager.is_debug_enabled('development') == True
    # Production should have debug disabled
    assert manager.is_debug_enabled('production') == False
    
    # Hosts should be different
    dev_host = manager.get_database_host('development')
    prod_host = manager.get_database_host('production')
    assert dev_host != prod_host
    
    print("Environment differences test passed")

def test_configuration_validation():
    """Test configuration validation"""
    manager = ConfigManager()
    manager.load_config('data/dev_config.yaml')
    manager.load_config('data/prod_config.yaml')
    
    # Both should be valid
    assert manager.validate_config('development') == True
    assert manager.validate_config('production') == True
    
    # Non-existent environment should be invalid
    assert manager.validate_config('nonexistent') == False
    
    print("Configuration validation test passed")

if __name__ == '__main__':
    test_load_configurations()
    test_environment_differences()
    test_configuration_validation()
    print("\nAll tests passed!")

