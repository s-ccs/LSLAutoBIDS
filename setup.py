#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lsl_autobids", # Replace with your own username
    version="0.0.1",
    author="Benedikt Ehinger, Manpa Barman",
    author_email="benedikt.ehinger@vis.uni-stuttgart.de, manpa.barman97@gmail.com,",
    description="A python package to automate the conversion of LSL to BIDS format",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s-ccs/LSLAutoBIDS/tree/main/lsl_autobids",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # entry_points={
    # 'console_scripts': [
    #     'your_tool_name = your_package_name.project_tool:main',
    # ],
    # },
    python_requires='>=3.7',
    # include_package_data=True,  # includes files from MANIFEST.in in the package
)