#!/bin/sh
URLS=/tmp/urls.txt
URLS_TMP=/tmp/urls.txt.tmp
CMD=wget
command -v curl > /dev/null 2>&1 && CMD=curl
if [ ! -f $URLS ]; then
    $CMD http://s3.amazonaws.com/alexa-static/top-1m.csv.zip > top-1m.csv.zip
    unzip -p top-1m.csv.zip | awk -F',' '{print $2}' > $URLS_TMP
    rm top-1m.csv.zip
    head -n 100000 $URLS_TMP > $URLS
    rm $URLS_TMP
fi
DIR=`./downloadr.py create`
cat $URLS | xargs -I {} -n 1 -P 64 ./downloadr.py download {} $DIR
