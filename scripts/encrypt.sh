#!/bin/bash

TOKEN="robinhood.pickle"
TOKEN_DIR="${HOME}/.tokens"
diff "${TOKEN_DIR}/${TOKEN}" ${TOKEN}
NEW_TOKEN=$?

# If Robinhood API grants us a new token:
if [[ ${NEW_TOKEN} == 1 ]]; then 
    echo new token
    # rm 
    # Encrypt token
    gpg --batch --yes --symmetric --cipher-algo AES256 --passphrase=${PASSWORD} --output "${TOKEN}.gpg" "${TOKEN_DIR}/${TOKEN}"
else
    echo no change
fi

# Remove leftover tokens
rm -rf ${TOKEN_DIR}
rm ${TOKEN}
