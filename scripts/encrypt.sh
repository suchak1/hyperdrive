#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"
NEW_TOKEN=$(diff "${TOKEN_DIR}/${TOKEN}\
" ${TOKEN} && echo false || echo true)

# If Robinhood API grants us a new token:
if [[ ${NEW_TOKEN} == true ]]; then 
    # Encrypt token
    gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase=${PASSWORD} ${TOKEN}
fi

# Remove leftover tokens
rm -rf ${TOKEN_DIR}
rm ${TOKEN}
