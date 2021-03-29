#!/bin/bash

# shellcheck disable=SC2011
ls ../data/doc/ \
  | xargs -I {} xmllint --html --xpath "//body//text()" "../data/doc/{}" 2>/dev/null \
  | sed -n 's/[^A-Za-z\s\Sа-яА-Я0-9]/ /pg'\
  | sed -n 's/[\x5C]/ /pg'\
  | tr -s " " \
  | tr " " "\n" \
  | sed -n '/[0-9]/!p'\
  | awk '{ if (length($0) > 2) print }'\
  | awk '{ if (length($0) < 13) print }'\
  | sed -n '/[a-z][A-Z]/!p'\
  | sed -n '/[а-я][А-Я]/!p'\
  | sort -u \
  > $1