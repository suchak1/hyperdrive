import os
import re
import requests
import subprocess

filename = 'requirements.txt'
new_packages = []
# we skip these because models may act unpredictably between versions
# must be updated manually
packages_to_skip = [
    # not supported - https://github.com/automl/auto-sklearn/blob/7eb667967c9f81de7cde5975024c858dd26982e2/requirements.txt#L9
    'scikit-learn',
    'auto-sklearn',
    # requires scikit-learn v1 - https://imbalanced-learn.org/stable/whats_new.html#version-0-9-0
    'imbalanced-learn',
    # not supported - https://github.com/automl/auto-sklearn/issues/1582
    # https://github.com/automl/auto-sklearn/blob/7eb667967c9f81de7cde5975024c858dd26982e2/requirements.txt#L19
    'pynisher',
    # numpy >= 1.24 does not have attribute warnings
    # https://stackoverflow.com/questions/74863592/attributeerror-module-numpy-has-no-attribute-warnings
    'numpy',
    # 'DataFrame' object has no attribute 'iteritems' => with pandas >= 2
    'pandas'
]
pattern = r'(\S*)\s?==\s?(\S*)'

with open(filename, 'r') as file:
    for line in file:
        match = re.match(pattern, line)
        line = line.strip()
        if match:
            package, version = match.groups()
            response = requests.get(f'https://pypi.org/pypi/{package}/json')
            keys = response.json()['releases'].keys()
            releases = [key for key in keys if key.replace('.', '').isdigit()]
            latest = sorted(
                releases,
                key=lambda release: [
                    int(number) for number in release.split('.')
                ]).pop()
            if latest != version and package not in packages_to_skip:
                print(f'Upgrading {package} ({version} => {latest})')
                CI = os.environ.get('CI')
                python = 'python' if CI else 'python3'
                cmd = f'{python} -m pip install {package}=={latest}'
                code = subprocess.run(cmd, shell=True).returncode
                if code:
                    exit(code)
                version = latest

            new_packages.append({'package': package, 'version': version})
        elif line:
            new_packages.append({'package': line})

with open(filename, 'w') as file:
    for package in new_packages:
        prefix = package['package']
        suffix = f"{' == ' + package['version'] if 'version' in package else ''}\n"
        file.write(f"{prefix}{suffix}")
