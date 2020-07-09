#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"

# Make tokens dir
if [[ $CI == true ]]; then
    mkdir "${TOKEN_DIR}"
else
# Load env vars
    set -a
    . ./.env
    set +a
fi

# Decrypt token
gpg --quiet --batch --yes --decrypt --passphrase="${PASSWORD}" --output "${TOKEN_DIR}/${TOKEN}" "${TOKEN}.gpg"

# Copy Robinhood token back to project dir
if [[ $CI == true ]]; then
    cp "${TOKEN_DIR}/${TOKEN}" ./
fi
