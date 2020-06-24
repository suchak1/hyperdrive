#!/bin/bash

# Load environment variables
set -a
. ./.env
set +a

# Encrypt Robinhood token
# cat robinhood.pickle