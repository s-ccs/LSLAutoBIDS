import argparse
import os
from .processing import check_for_new_data
from .folder_config import PROJECT_ROOT, PROJECT_NAME

if __name__ == "__main__":


    # Write an argument parser which takes the project name as argument while running the script
    argparser = argparse.ArgumentParser(description='Get the project name')
    # give a -p or --project_name argument to the script
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    args = argparser.parse_args()

    #take the project name and find the project in the project directory and print project not found if the path doesnot exist
    project_name = args.project_name
    if project_name == PROJECT_NAME:
        project_path = os.path.join(PROJECT_ROOT,PROJECT_NAME)
        if not os.path.exists(project_path):
            print('Project not found')
            exit() 
        print('Project found')
        check_for_new_data(project_path)

    else: 
        print('Project not specified correctly')
        exit()
    