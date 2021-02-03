import os
import requests
from dotenv import load_dotenv, find_dotenv
from setuptools import setup, find_packages


load_dotenv(find_dotenv('config.env'))


def get_version():
    url = 'https://api.github.com/repos/suchak1/hyperdrive/releases/latest'
    token = os.environ.get('GITHUB')
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers if token else None)
    data = response.json()
    version = data['tag_name'].replace('v', '')
    return version


def get_requirements():
    with open('requirements.txt', 'r') as file:
        return [line.strip() for line in file if line]


def get_readme():
    with open("README.md", "r") as file:
        return file.read()


setup(
    name='hyperdrive',
    version=get_version(),
    description='An algorithmic trading platform',
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/suchak1/hyperdrive',
    author='Krish Suchak',
    author_email='suchak.krish@gmail.com',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=get_requirements(),
    project_urls={
        'Bug Reports': 'https://github.com/suchak1/hyperdrive/issues',
        'Source': 'https://github.com/suchak1/hyperdrive'
    }
)
