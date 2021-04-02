#!/bin/bash

# shellcheck disable=SC2011
cat $1 \
  | sed -n 's/[^A-Za-z\s\Sа-яА-Я0-9]/ /pg'\
  | sed -n 's/[\x5C]/ /pg'\
  | tr -s " " \
  | tr " " "\n" \
  | sed -n '/[0-9]/!p'\
  | awk '{ if (length($0) > 2) print }'\
  | awk '{ if (length($0) < 13) print }'\
  | sed -n '/[a-z][A-Z]/!p'\
  | sed -n '/[а-я][А-Я]/!p'\
  | sort -u