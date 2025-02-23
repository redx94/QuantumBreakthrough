from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import os
from pydantic import BaseModel, validator, Field
from dataclasses import dataclass

@dataclass
class GlobalConfig:
    """Global configuration settings for the quantum breakthrough project."""
    environment_settings: Dict[str, Any]
    model_settings: Dict[str, Any]
    logging_settings: Dict[str, Any]
    security_settings: Dict[str, Any]

    @classmethod
    def from_yaml(cls, config_path: str) -> 'GlobalConfig':
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        return cls(
            environment_settings=config_data.get('environment', {}),
            model_settings=config_data.get('model', {}),
            logging_settings=config_data.get('logging', {}),
            security_settings=config_data.get('security', {})
        )

class EnvironmentSettings(BaseModel):
    num_qubits: int
    noise_level: float
    max_steps: int
    reward_threshold: float

    @validator('num_qubits')
    def validate_num_qubits(cls, v):
        if not 1 <= v <= 20:
            raise ValueError("num_qubits must be between 1 and 20")
        return v

class QuantumSettings(BaseModel):
    num_qubits: int = Field(gt=0, lt=50)
    noise_level: float = Field(gt=0.0, lt=1.0)
    optimization_level: int = Field(ge=0, le=3)
    
class SecuritySettings(BaseModel):
    encryption_algorithm: str
    key_rotation_days: int = Field(gt=0)
    
class GlobalSettings(BaseModel):
    quantum: QuantumSettings
    security: SecuritySettings
    environment: Dict[str, Any]
    
    class Config:
        validate_assignment = True
        extra = "forbid"

class Settings:
    """Global settings management."""
    
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.yaml"
        self.settings = self.load_config()
        self._load_environment_variables()
        self._validate_settings()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return self.create_default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        default_config = {
            'environment': {
                'num_qubits': 2,
                'noise_level': 0.01,
                'max_steps': 100,
                'reward_threshold': 0.95
            },
            'training': {
                'learning_rate': 0.001,
                'batch_size': 64,
                'episodes': 1000
            },
            'logging': {
                'level': 'INFO',
                'file': 'quantum_breakthrough.log'
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f)
        
        return default_config

    def _load_environment_variables(self):
        """Override settings with environment variables."""
        env_prefix = "QUANTUM_"
        for key in os.environ:
            if key.startswith(env_prefix):
                setting_path = key[len(env_prefix):].lower().split("_")
                self._update_nested_dict(self.settings, setting_path, os.environ[key])

    def _update_nested_dict(self, d: dict, keys: list, value: Any):
        """Update nested dictionary with value at path specified by keys."""
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = self._convert_value(value)

    @staticmethod
    def _convert_value(value: str) -> Any:
        """Convert string values to appropriate types."""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value if value.lower() not in ['true', 'false'] else value.lower() == 'true'

    def _validate_settings(self):
        """Validate settings using pydantic models."""
        self.environment_settings = EnvironmentSettings(**self.settings['environment'])
