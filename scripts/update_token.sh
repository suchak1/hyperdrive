#!/bin/bash

DIR_WIN="/mnt/c/Users/Krish Suchak/.tokens/"
DIR_LIN="${HOME}/.tokens/"
FILE="robinhood.pickle"

# If we are in not in CI environment:
if [[ $CI != "true" ]]; then
    
    # Find most recent token on PC and update the older version
    # (either on Windows or Linux)
    if [[ "${DIR_WIN}${FILE}" -nt "${DIR_LIN}${FILE}" ]]; then
        cp "${DIR_WIN}${FILE}" "${DIR_LIN}"
        echo Copied Robinhood oauth token from Windows to Linux.
    else
        cp "${DIR_LIN}${FILE}" "${DIR_WIN}"
        echo Copied Robinhood oauth token from Linux to Windows.
    fi

    # Perform tests (thus updating token if necessary)
    python -m pytest -vv

    # Copy Robinhood token to project dir
    cp "${DIR_WIN}${FILE}" ./

    # Load env vars
    set -a
    . ./.env
    set +a

    # Encrypt token
    gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase="${PASSWORD}" "${FILE}"

    # Remove token
    rm "${FILE}"

# If we are in CI enviroment:
else
    # Make tokens dir
    mkdir "${HOME}/.tokens"

    # Decrypt token
    gpg --quiet --batch --yes --decrypt --passphrase="${PASSWORD}" --output "${HOME}/.tokens/${FILE}" "${FILE}.gpg"

    # Perform tests (thus updating token if necessary)
    python -m pytest -vv

    # Copy Robinhood token back to project dir
    cp "${HOME}/.tokens/${FILE}" ./

    # Encrypt token
    gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase="${PASSWORD}" "${FILE}"

    # Remove leftover tokens
    rm -rf "${HOME}/.tokens"
    rm "${FILE}"

# if git diff and branch == master,
# commit and push
# master branch: daily
# consider just running pytest init here 
# find a way to fail it if gpg doesn't exist
# and adding pytest --vv as separate step in yml
# consider moving non ci logic out
# consider splitting ci logic into pre and post test scripts
# pre script updates token 
# test
# post scripts clean up
    echo hi
fi
