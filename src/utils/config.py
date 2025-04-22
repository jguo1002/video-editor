import os
import yaml


def load_config(config_path: str) -> dict:
    """
    Loads the configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML config file.

    Returns:
        dict: The configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        YAMLError: If there is an error in parsing the YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML: {e}")
