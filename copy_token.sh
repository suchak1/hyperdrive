#!/bin/bash

DIR_WIN="/mnt/c/Users/Krish Suchak/.tokens/"
DIR_LIN="${HOME}/.tokens/"
FILE="robinhood.pickle"

if [[ "${DIR_WIN}${FILE}" -nt "${DIR_LIN}${FILE}" ]]; then
    cp "${DIR_WIN}${FILE}" "${DIR_LIN}"
    echo Copied robinhood auth token from Windows to Linux.
else
    cp "${DIR_LIN}${FILE}" "${DIR_WIN}"
    echo Copied robinhood auth token from Linux to Windows.
fi