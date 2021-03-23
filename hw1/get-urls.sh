#!/bin/bash

orifinal="http://www.adm.nov.ru/page/38300"
datadir="../data"
urlfile="$datadir/urls.txt"

curl -s $orifinal | xmllint --html --xpath '//div[@id="content"]//p//a/@href' --nowarning  2>/dev/null - | sed -n "s/^\s*href=\x22\(.*\)\x22\s*$/\1/p" > $urlfile

index="../index.txt"
n=1
rm $index
while read p; do
  curl -L -s $p 2>/dev/null > "$datadir/doc/$n.html"
  echo "$n. $p" >> $index
  n=$((n + 1))
done <$urlfile

zip -r -9 docs.zip "$datadir/doc/*"