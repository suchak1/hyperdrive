
#!/bin/bash

BRANCH=$1
git diff --stat master "${BRANCH}"