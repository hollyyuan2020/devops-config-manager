# DevOps Configuration Manager

Simple tool for managing application configurations across development environments.

## Environments

- **dev**: Development environment (localhost, debug enabled)
- **staging**: Testing environment (staging servers, production-like)  
- **prod**: Production environment (live servers, high performance)

## Usage

### Load and Compare Configurations
```python
from src.config_manager import ConfigManager

# Load configurations
manager = ConfigManager()
manager.load_config('data/dev_config.yaml')
manager.load_config('data/prod_config.yaml')

# Compare environments
differences = manager.compare_configs('development', 'production')
print(f"Found {len(differences)} differences")

