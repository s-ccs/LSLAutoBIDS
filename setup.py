from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()
setup(
    name='LSLAutoBIDS',
    version='0.1.0',
    description='Tools to convert LSL + friends automatically to BIDS, and upload to a Dataverse',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/s-ccs/LSLAutoBIDS',
    packages=find_packages(include=['lsl_autobids', 'lsl_autobids.*']),
    install_requires= #requirements,
    [
        # List your dependencies here, e.g.,
        'pyxdf',
        'mne',
        'mne-bids',
        'bids_validator==1.13.1',
        'datalad-dataverse==1.0.1',
        'datalad-installer==1.0.3',
        'pyDataverse==0.3.1',
        'requests>=2.12.0',
        'jsonschema>=3.2.0',
        'AnnexRemote@git+https://github.com/Lykos153/AnnexRemote.git@master#egg=AnnexRemote',
        'toml',
        'pyyaml',
        'mnelab',
        'pybv',
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
