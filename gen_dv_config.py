# Write a python script to generate the dataverse.json file with the help of gen_dv_config.py

import yaml

# Create a dictionary representing the template data with comments
template_data = {
    "BASE_URL": "https://darus.uni-stuttgart.de",  # The base URL for the service.
    "API_TOKEN": "# Paste your API token here",    # Your API token for authentication.
    "PARENT_DATAVERSE_NAME": "simtech_pn7_computational_cognitive_science"     # The name of the program or service.
}

# Specify the filename for the YAML file
template_filename = "dataverse_config.yaml"

# Write the template data to the YAML file
with open(template_filename, "w") as template_file:
    yaml.dump(template_data, template_file)

print(f"Template YAML file '{template_filename}' has been created.")