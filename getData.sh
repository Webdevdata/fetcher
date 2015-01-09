#!/bin/sh
TRAIL='http://s3.amazonaws.com/alexa-static'
ZIP='top-1m.csv.zip'
URLS_FILE='/tmp/urls.txt'
URLS_TEMP="${URLS_FILE}.tmp"

if [ ! -f $URLS_FILE ]; then
    if command -v curl >/dev/null 2>&1; then
        DOWNLOAER="curl --output"
    elif command -v wget >/dev/null 2>&1; then
        DOWNLOAER="wget --output-document"
    else
        echo Cannot find curl or wget
        exit 42
    fi
    $DOWNLOAER $ZIP $TRAIL/$ZIP
    unzip -p $ZIP | awk -F',' '{print $2}' > $URLS_TEMP
    rm $ZIP
    head -n 100000 $URLS_TEMP > $URLS_FILE
    rm $URLS_TEMP
fi

DIR=`./downloadr.py create`
cat $URLS_FILE | xargs -I {} -n 1 -P 64 ./downloadr.py download {} $DIR
