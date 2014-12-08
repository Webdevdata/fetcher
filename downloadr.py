#!/usr/bin/env python
import os
from time import gmtime, strftime
import sys
from urllib2 import HTTPError, URLError, urlopen
import hashlib
import magic
import logging


def createDir():
    dirname = "webdevdata.org-" + strftime("%Y-%m-%d-%H%M%S", gmtime())
    os.mkdir(dirname)
    return dirname


def connect(url):
    try:
        try:
            f = urlopen("http://" + url)
            return f
        except URLError, e:
            try:
                f = urlopen("https://" + url)
                return f
            except URLError, e:
                try:
                    f = urlopen("http://www." + url)
                    return f
                except URLError, e:
                    try:
                        f = urlopen("https://www." + url)
                        return f
                    except:
                        raise
    except HTTPError, e:
        log("HTTPError: " + str(e.code) + " " + str(url))
    except URLError, e:
        log("URLError: " + str(e.reason) + " " + str(url))
    except Exception, e:
        log(str(e) + " " + str(url))


def download_file(url, dir):
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        filename=os.path.join(dir, 'log.txt'))
    os.chdir(dir)
    url = url.strip()
    print "Downloading: ", url
    if url.startswith("http://"):
        url = url[7:]
    if url.startswith("https://"):
        url = url[8:]
    urlhost = url.split("/")[0]
    root = connect(urlhost)
    if root:
        try:
            hash = hashlib.md5()
            hash.update(url)
            dir = hash.hexdigest()[:2]
            if not os.path.exists(dir):
                os.mkdir(dir)
            buffer = root.read()
            ext = magic.from_buffer(buffer).split()[0].lower()
            if "html" in ext:
                ext = "html.txt"
            filename = dir + "/" + urlhost + "_" + hash.hexdigest() + "." + ext
            with open(filename, "wb") as local_file:
                local_file.write(buffer)
                local_file.close()
            with open(filename + ".hdr.txt", "wb") as local_file:
                local_file.write(str(root.getcode()) + "\n" + str(root.info()))
                local_file.close()
        except Exception, e:
            log(str(e) + " " + str(url))


def log(message):
    logging.error(message)
    print message


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print >>sys.stderr, \
                "Usage:", sys.argv[0], "create|download", "<URL>", "<dir>"
            quit()
        command = sys.argv[1]
        if command == "create":
            print createDir()
        elif command == "download":
            if len(sys.argv) < 4:
                print >>sys.stderr, "Where's the URL and the directory?"
                quit()
            download_file(sys.argv[2], sys.argv[3])
        else:
            print >>sys.stderr, "Didn't understand the command", command
    except KeyboardInterrupt:
        pass
