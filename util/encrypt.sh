#!/bin/bash

FILE="${1}"

if [[ $CI != true ]]; then
    source config.env   
fi

# Regex to auto encrypt on save: "^.*\/encrypted\/(?!.*[.]gpg$).*$"
# using Run on Save VSCode extension authored by emeraldwalk
gpg --batch --yes --symmetric --cipher-algo AES256 --passphrase=${RH_PASSWORD} --output "${FILE}.gpg" "${FILE}"
