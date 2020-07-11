#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"


if [[ $CI == true ]]; then
    # Make tokens dir
    mkdir "${TOKEN_DIR}"
    # Remote output path
    OUTPUT="${TOKEN_DIR}/${TOKEN}"
else
    # Local output path
    OUTPUT="./${TOKEN}"
    # Load env vars
    set -a
    . ./.env
    set +a
fi

# Decrypt token
gpg --quiet --batch --yes --decrypt --passphrase="${PASSWORD}" --output "${OUTPUT}" "${TOKEN}.gpg"

# Copy Robinhood token back to project dir
if [[ $CI == true ]]; then
    cp "${TOKEN_DIR}/${TOKEN}" ./
fi
