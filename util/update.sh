if [[ $SOURCE == LOCAL ]]; then
    # Sync local tokens
    util/sync.sh

    # Decrypt remote token
    util/decrypt.sh

    # Encrypt local token
    util/encrypt.sh
else
    if [[ $SOURCE == REMOTE ]]; then
        # Get latest encrypted token from remote repo
        git checkout upstream/master -- robinhood.pickle.gpg

        # Decrypt remote token
        util/decrypt.sh

        # Sync local tokens
        util/sync.sh
    else
        echo SOURCE of latest token must be specified.
    fi
fi
