import os


def get_api_key(key_name, env_file=None):
    # If no specific env file is provided, use the one in the root directory
    if env_file is None:
        # Get the py-projects root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(root_dir, '.env')

    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                # Parse key-value pairs
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    # If this is the key we're looking for
                    if key == key_name:
                        # Remove quotes if present
                        return value.strip().strip("\"'")

        # Key not found
        return None
    except FileNotFoundError:
        print(f"Warning: {env_file} file not found.")
        return None
