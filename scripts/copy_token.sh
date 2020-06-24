#!/bin/bash

DIR_WIN="/mnt/c/Users/Krish Suchak/.tokens/"
DIR_LIN="${HOME}/.tokens/"
FILE="robinhood.pickle"

# If we are in CI enviroment, 
# Find most recent token on PC and update the older version
# (either on Windows or Linux)
if [[ "${DIR_WIN}${FILE}" -nt "${DIR_LIN}${FILE}" ]]; then
    cp "${DIR_WIN}${FILE}" "${DIR_LIN}"
    echo Copied Robinhood oauth token from Windows to Linux.
else
    cp "${DIR_LIN}${FILE}" "${DIR_WIN}"
    echo Copied Robinhood oauth token from Linux to Windows.
fi

if [[ $CI == "true" ]]; then
# decrypt robinhood.gpg
# mv to home/.tokens
# perform tests
# mv back to scarlett/ -this file
# encrypt -this file
# if git diff,
# commit and push
    echo hi
fi

# copy Robinhood token to project dir
cp "${DIR_WIN}${FILE}" ./

# encrypt Robinhood token
scripts/encrypt_token.sh