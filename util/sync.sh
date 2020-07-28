#!/bin/bash

USERNAME=$(cmd.exe /C "echo %USERNAME%" | tr -d '\r')
DIR_WIN="/mnt/c/Users/${USERNAME}/.tokens/"
DIR_LIN="${HOME}/.tokens/"
FILE="robinhood.pickle"

# Find most recent token on PC and update the older version
# (either on Windows or Linux)
if [[ "${DIR_WIN}${FILE}" -nt "${DIR_LIN}${FILE}" ]]; then
    cp "${DIR_WIN}${FILE}" "${DIR_LIN}"
    echo Copied Robinhood OAuth token from Windows to Linux.
else
    cp "${DIR_LIN}${FILE}" "${DIR_WIN}"
    echo Copied Robinhood OAuth token from Linux to Windows.
fi

# # Update the token if necessary
# python scripts/login.py

# # Copy Robinhood token to project dir
# cp "${DIR_WIN}${FILE}" ./

# # Load env vars
# set -a
# . ./.env
# set +a

# Encrypt token
gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase=${RH_PASSWORD} ${FILE}

# # Remove token
# rm "${FILE}"
