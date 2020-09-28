# get total lines of code

git ls-files | xargs cat | wc -l
# git ls-files | xargs wc -l
# git diff --stat `git hash-object -t tree /dev/null`
