info = """
# Information of the configuration file:  
# The configuration file is a YAML file that contains the following fields:
#    BIDS_ROOT: Set up the BIDS output path - it is referenced from the home directory of your PC. 
#    For example, if your home directory is /home/username and you have a /home/username/data/bids directory where you have the 
#    BIDS data in the home directory then the BIDS_ROOT path will be 'data/bids/'
#    PROJECT_ROOT: This is the actual path to the directory containing xdf files
#    PROJECT_STIM_ROOT: This is the actual path to the directory containing the stimulus files
#    BASE_URL: The base URL for the dataverse service.
#    API_KEY: Your API token for authentication - you can get it from the dataverse service.
#    PARENT_DATAVERSE_NAME: The name of the program or service.
#
# Important: all paths + API_KEY need to be placed in quotes!

"""

# imports
import yaml
import os
# import argparse

# Create a dictionary representing the template data with comments
template_data = {
       
    "BIDS_ROOT": "# relative to home: workspace/projects/LSLAutoBIDS/data/bids/",       
    "PROJECT_ROOT" : "# relative to home: workspace/projects/LSLAutoBIDS/data/projects/", 
    "PROJECT_STIM_ROOT" : "# path relative to home: workspace/projects/LSLAutoBIDS/data/project_stimulus/", 
    "BASE_URL": "https://darus.uni-stuttgart.de",  # The base URL for the service.
    "API_KEY": "# Paste your dataverse API token here",    # Your API token for authentication.
    "PARENT_DATAVERSE_NAME": "simtech_pn7_computational_cognitive_science"     # The name of the program or service.
}


def main():


    # # Comment out the following if you want a custom path for the configuration file as argument

    # argparser = argparse.ArgumentParser(description='Get the config path')
    # argparser.add_argument('-p','--configpath', default=os.path.join(os.path.expanduser("~"),'autobids_config.yaml'),type=str, help='Enter the config path')
    # args = argparser.parse_args()

    # # Specify the filename for the YAML file
    # config_path =args.configpath 

    # # Save the configuration path to the config_info.yaml file
    # with open('./config_info.yaml') as f:
    #     data = yaml.safe_load(f)

    # data['CONFIG_PATH'] = config_path
    # with open('./config_info.yaml', 'w') as f:
    #     yaml.dump(data, f)


    config_path = os.path.join(os.path.expanduser("~"),'.config/lslautobids/autobids_config.yaml')

    # Check if the YAML file already exists and fill the fields
    try:
        with open(config_path, "r") as template_file:
            print(f"The file '{config_path}' already exists.")
            while True:
                print("Do you want to view the fields of the file? (yes/no): ")
                view = input()
                if view.lower() == "yes" or view.lower() == "y":
                    print("The fields of the file are:")
                    print(template_file.read())
                    break
                elif view.lower() == "no" or view.lower() == "n":
                    print("The fields of the file will not be displayed.")
                    break
                else:
                    print("Invalid input. Please enter a valid input.")
            while True:
                print("Do you want to overwrite the file? (yes/no): ")
                overwrite = input()
                if overwrite.lower() == "yes" or overwrite.lower() == "y":
                    print("The file will be overwritten.")
                    with open(config_path, "w") as template_file:
                        template_file.write(info)
                        yaml.dump(template_data, template_file)
                    print(f"""Template YAML file '{config_path}' has been overwritten with the default template. Please go to 
                          {config_path} and fill in the fields.""")
                    break
                elif overwrite.lower() == "no" or overwrite.lower() == "n":
                    print("The file will not be overwritten.")
                    break
                else:
                    print("Invalid input. Please enter a valid input.")
    except FileNotFoundError:
        # Write the template data to the YAML file
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as template_file:
            yaml.dump(template_data, template_file)

        print(f"Template YAML file '{config_path}' has been created. Fill in the fields in the file.")

if __name__ == "__main__":
    main()
