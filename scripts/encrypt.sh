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


    
# if git diff (decrypted versions) and branch == master,
# commit and push
# master branch: daily
# consider just running pytest init here (build.py -> starts Scarlett)


# 1. git commit and push if pull request -> then change to amster
# 2. schedule every 5 min => then schedule daily build
# 3. init function only
# 4. separate update and test steps, so that token updates daily regardless of tests passing
# 5. finish pytest tests
# 6. update version
# 7. consider making changelog


# https://help.github.com/en/actions/reference/events-that-trigger-workflows#scheduled-events-schedule

# - * * * * *
# - 0 0 * * 0
# make ticket for code coverage
# make ticket for defining buy and hold strat
# make ticket for generating ascii table report with colors
#  - sharpe, drowndown, other metrics