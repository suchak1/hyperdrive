if [[ $SOURCE == LOCAL ]]; then
    # Sync local tokens
    scripts/sync.sh

    # Decrypt remote token
    scripts/decrypt.sh

    # Encrypt local token
    scripts/encrypt.sh
else
    if [[ $SOURCE == REMOTE ]]; then
        # Get latest encrypted token from remote repo
        git checkout upstream/master -- robinhood.pickle.gpg

        # Decrypt remote token
        scripts/decrypt.sh

        # Sync local tokens
        scripts/sync.sh
    else
        echo SOURCE of latest token must be specified.
    fi
fi
