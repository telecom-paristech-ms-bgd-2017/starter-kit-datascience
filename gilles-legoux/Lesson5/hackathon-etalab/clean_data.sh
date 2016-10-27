#!/usr/bin/env bash

pathname="$1"
path=`dirname $1`
fname=`basename $1`
ext="${fname##*.}"
fname="${fname%.*}"

# convert to UTF-8 encoding
# see encoding with file -i <filename>
encoding=`file -i "$1" | cut -f2 -d '='`
iconv -f "${encoding}" -t UTF-8 "${1}" -o "${path}/${fname}-utf8.${ext}"

# convert to unix end line \n
# see dos line cat -vet <filename>
dos2unix -n "${path}/${fname}-utf8.${ext}" "${path}/${fname}-utf8-unix.${ext}"
