#!/usr/bin/env python

import os
from time import gmtime, strftime
import sys
from urllib2 import HTTPError, URLError, urlopen
import hashlib
import magic

def createDir():
    dirname = "webdevdata.org-" + strftime("%Y-%m-%d-%H%M%S", gmtime())
    os.mkdir(dirname)
    return dirname

def connect(url):
    try:
        f = urlopen("http://" + url);
        return f;
    except URLError, e:
        try:
            f = urlopen("https://" + url);
            return f;
        except URLError, e:
            try:
                f = urlopen("http://www." + url);
                return f;
            except URLError, e:
                try:
                    f = urlopen("https://www." + url);
                    return f;
                except HTTPError, e:
                    print "HTTPError:", e.code, url
                except URLError, e:
                    print "URLError:", e.reason, url

def downloadFile(url, dir):
    os.chdir(dir)
    url = url.strip()
    try:
        print "Downloading: ", url
        if url.startswith("http://"):
            url = url[7:]
        if url.startswith("https://"):
            url = url[8:]
        urlhost = url.split("/")[0]
        urlpath = "/".join(url.split("/")[1:])
        f = connect(urlhost);
        hash = hashlib.md5()
        hash.update(url)
        dir = hash.hexdigest()[:2]
        if not os.path.exists(dir):
            os.mkdir(dir)
        buffer = f.read()
        ext = magic.from_buffer(buffer).split()[0].lower()
        if "html" in ext:
            ext = "html.txt"
        filename = dir + "/" + urlhost + "_" + hash.hexdigest() + "." + ext
        with open(filename, "wb") as local_file:
            local_file.write(buffer)
            local_file.close()
        with open(filename + ".hdr.txt", "wb") as local_file:
            local_file.write(str(f.getcode()) + "\n" + str(f.info()))
            local_file.close()
    except HTTPError, e:
        print "HTTPError:", e.code, url
    except URLError, e:
        print "URLError:", e.reason, url

if __name__=="__main__":
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage:", sys.argv[0], "create|download", "<URL>", "<dir>"
        quit()
    command = sys.argv[1]
    if command == "create":
        print createDir()
    elif command == "download":
        if len(sys.argv) < 4:
            print >>sys.stderr, "Where's the URL and the directory?"
            quit()
        downloadFile(sys.argv[2], sys.argv[3])
    else:
        print >>sys.stderr, "Didn't understand the command", command
