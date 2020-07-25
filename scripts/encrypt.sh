#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"
diff "${TOKEN_DIR}/${TOKEN}" ${TOKEN}
NEW_TOKEN=$?

# If Robinhood API grants us a new token:
if [[ ${NEW_TOKEN} == 1 ]]; then 
    # Encrypt token
    gpg --batch --yes --symmetric --cipher-algo AES256 --passphrase=${RH_PASSWORD} --output "${TOKEN}.gpg" "${TOKEN_DIR}/${TOKEN}"
fi

# Remove leftover tokens
rm -rf ${TOKEN_DIR}
rm ${TOKEN}
