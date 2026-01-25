"""
Environment configurations for different testing environments
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class EnvironmentConfig:
    """Environment configuration data class"""
    name: str
    base_url: str
    api_url: str = ""
    username: str = ""
    password: str = ""
    timeout: int = 30


class Environments:
    """Environment configurations for different testing environments"""

    # Predefined environments
    _environments: Dict[str, EnvironmentConfig] = {
        "dev": EnvironmentConfig(
            name="Development",
            base_url="https://dev.saucedemo.com",
            api_url="https://api.dev.saucedemo.com",
            username="standard_user",
            password="secret_sauce",
            timeout=30
        ),
        "staging": EnvironmentConfig(
            name="Staging",
            base_url="https://staging.saucedemo.com",
            api_url="https://api.staging.saucedemo.com",
            username="standard_user",
            password="secret_sauce",
            timeout=30
        ),
        "prod": EnvironmentConfig(
            name="Production",
            base_url="https://www.saucedemo.com",
            api_url="https://api.saucedemo.com",
            username="standard_user",
            password="secret_sauce",
            timeout=30
        ),
        "local": EnvironmentConfig(
            name="Local",
            base_url="http://localhost:8080",
            api_url="http://localhost:8081",
            username="admin",
            password="admin123",
            timeout=10
        )
    }

    @classmethod
    def get(cls, env_name: str) -> Optional[EnvironmentConfig]:
        """Get environment configuration by name"""
        return cls._environments.get(env_name.lower())

    @classmethod
    def add(cls, env_name: str, config: EnvironmentConfig):
        """Add a new environment configuration"""
        cls._environments[env_name.lower()] = config

    @classmethod
    def list_environments(cls) -> list:
        """List all available environments"""
        return list(cls._environments.keys())

    @classmethod
    def get_default(cls) -> EnvironmentConfig:
        """Get default environment (production)"""
        return cls._environments["prod"]
