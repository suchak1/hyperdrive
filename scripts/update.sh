# Get latest encrypted token from remote repo
git checkout upstream/master -- robinhood.pickle.gpg

# Decrypt remote token
scripts/decrypt.sh

# Sync local tokens
scripts/sync.sh
