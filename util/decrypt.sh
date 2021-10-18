#!/bin/bash

FILE="${1}"

if [[ $CI != true ]]; then
    source config.env   
fi

# Decrypt
gpg --verbose --batch --yes --decrypt --passphrase=${RH_PASSWORD} --output "${FILE}" "${FILE}.gpg"