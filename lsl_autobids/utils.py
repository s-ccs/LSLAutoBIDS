# utils.py
import logging
import toml
import os
import tomllib

def get_user_input(prompt: str, max_attempts: int = 5) -> str:
    """Prompt the user with a yes/no question and validate the input.

    Args:
        prompt (str): The question to display to the user.
        max_attempts (int): Number of allowed retries for invalid input.

    Returns:
        str: 'y' or 'n'

    Raises:
        ValueError: If the user fails to provide valid input.
    """
    valid_inputs = {'y', 'n'}
    for attempt in range(max_attempts):
        user_input = input(f"{prompt} (y/n): ").strip().lower()
        if user_input in valid_inputs:
            return user_input
        logging.warning(f"Invalid input. {max_attempts - attempt - 1} attempt(s) remaining.")
    raise ValueError("Maximum attempts exceeded. Invalid user input.")

def read_toml_file(toml_file):
    if not isinstance(toml_file, (str, bytes, os.PathLike)):
        raise TypeError(f"Expected a path-like object, got {type(toml_file).__name__}")

    with open(toml_file, 'rb') as file:
        return tomllib.load(file)

    
def write_toml_file(toml_file, data):
    with open(toml_file, 'w') as file:
        toml.dump(data, file)
        
