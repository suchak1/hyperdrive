import os
import re
import requests
import subprocess

filename = 'requirements.txt'
new_packages = []

with open(filename, 'r+') as file:
    pattern = '(.*) == (.*)'
    packages = re.findall(pattern, file.read())
    for package, version in packages:
        response = requests.get(f'https://pypi.org/pypi/{package}/json')
        releases = response.json()['releases'].keys()
        latest = sorted(
            releases,
            key=lambda release: [
                int(
                    number
                ) for number in release.split('.') if number.isdigit()
            ]).pop()
        if latest != version:
            print(f'Upgrading {package} ({version} => {latest})')
            CI = os.environ.get('CI')
            python = 'python' if CI else 'python3'
            cmd = f'{python} -m pip install {package}=={latest}'
            code = subprocess.run(cmd, shell=True).returncode
            if code:
                exit(code)
            version = latest

        new_packages.append((package, version))

    for package, version in new_packages:
        file.write(f'{package} == {version}\n')
