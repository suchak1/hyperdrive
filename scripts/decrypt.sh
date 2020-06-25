#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"

# Make tokens dir
mkdir ${TOKEN_DIR}

# Decrypt token
gpg --quiet --batch --yes --decrypt --passphrase=${PASSWORD} --output "${TOKEN_DIR}/${TOKEN}" "${TOKEN}.gpg"

# Copy Robinhood token back to project dir
cp "${TOKEN_DIR}/${TOKEN}" ./