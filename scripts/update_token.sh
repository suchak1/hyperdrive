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

    # copy Robinhood token to project dir
    cp "${DIR_WIN}${FILE}" ./

    # Load env vars
    set -a
    . ./.env
    set +a

    # Encrypt token
    gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase="${PASSWORD}" "${FILE}"

    # Remove token
    rm robinhood.pickle

# If we are in CI enviroment:
else
    # Decrypt token
    gpg --quiet --batch --yes --decrypt --passphrase="${PASSWORD}" --output "${HOME}/.tokens/${FILE}" "${FILE}.gpg"

# decrypt robinhood.gpg
# mv to home/.tokens
# perform tests
# mv back to scarlett/ -this file
# encrypt -this file
# remove robinhood.pickle
# if git diff,
# commit and push
    echo hi
fi



# encrypt Robinhood token
