import os
import yaml
import logging

logger = logging.getLogger("utils")

# Absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_params(relative_path: str = "config/params.yaml") -> dict:
    try:
        config_path = os.path.join(PROJECT_ROOT, relative_path)

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")

        with open(config_path, "r") as file:
            params = yaml.safe_load(file)

        logger.debug("Loaded config from %s", config_path)
        return params

    except Exception as e:
        logger.error("Failed to load config: %s", e)
        raise