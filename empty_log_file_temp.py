def empty_text_file(file_path):
    """
    Empties the contents of a text file.
    
    Parameters:
        file_path (str): The path to the text file.
    """
    with open(file_path, 'w') as file:
        file.truncate(0)
    print(f"The contents of {file_path} have been emptied.")


# Example usage
file_path = './data/projects/sampleproject/last_run_log.txt'  # Replace with the actual file path
empty_text_file(file_path)
