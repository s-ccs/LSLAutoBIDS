from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name='lsl_autobids',
    version='0.1.0',
    description='Tools to convert LSL + friends automatically to BIDS, and upload to a Dataverse',
    author='Manpa Barman, Benedikt Ehinger',
    author_email='manpa.barman97@gmail.com, science@benediktehinger.de',
    url='https://github.com/s-ccs/LSLAutoBIDS',
    packages=find_packages(include=['lsl_autobids', 'lsl_autobids.*']),
    install_requires= requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
