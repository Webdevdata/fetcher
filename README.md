Fetcher
=======

Scripts used to fetch the HTML files from top Alexa sites.

Methodology
-----------

-   The top 1 million Alexa sites
    [csv](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip) is
    downloaded, unzipped, and the URLs are extracted from it.

    **Note:** only the top 100,000 sites are kept for downloding.

-   The URLs are then fed to a Python script that downloads the HTML
    files and their HTTP headers using a process pool (to minimize
    waiting).

    Errors are reported to a log file (as below).

Usage
-----

If you're on Linux or OS X, simply run `./getData.sh` and you should be
good to go. If you're on Windows, [cygwin](http://www.cygwin.com/) may
be your best bet.

If you want to fetch resources other than Alexa's top HTMLs, you can do
that by doing something like `cat resource_urls.txt | ./downloadr.py`

Dependencies
------------

-   Python (Tested with 2.7)
-   curl
-   zcat
-   [python-magic](https://github.com/ahupp/python-magic), which also
    requires [libmagic](http://www.darwinsys.com/file/) (which you can
    install via homebrew)

If you use [virtualenv](https://github.com/pypa/virtualenv), you can
install the required Python package locally:

-   `virtualenv venv`
-   `. venv/bin/activate`
-   `pip install -r requirements.txt`

Whenever you want to run this script, use:

-   `. venv/bin/activate`
-   `./getData.sh`

If you use [autoenv](https://github.com/kennethreitz/autoenv) the
activation step will be done automatically on entering the directory.

Results
-------

The resulting directory structure is:

-   A root directory of the pattern "webdevdata.org-YYYY-MM-DD-HHMMSS"
-   A "log.txt" file within this directory contains a list of errors
    encountered across all downloads.
-   Sub-directories are 16 bit hashes of the URLs below them. Used to
    verify there are not toom many files in a single directory.

The resulting files have an ".html.txt" extension for the data files and
".html.hdr.txt" extension for the header files.

-   **[October 2013 data set (780 Mb, .7z
    file)](http://www.html5accessibility.com/HTMLdata/webdevdata.org-2013-10-30.7z):**
    Includes approx 78,000 HTML files.
-   **[June 2013 data set (484 Mb, .7z
    file)](http://www.html5accessibility.com/HTMLdata/webdevdata.org-2013-06-18.7z):**
    Includes approx 53,000 HTML files. Some HTML element and attribute
    [usage
    stats](https://docs.google.com/spreadsheet/ccc?key=0AlVP5_A996c5dFhMQ3R2SG1uZFNZVEsxUURQN213VVE#gid=0)
    derived from the data are available.

Queries
-------

A java based script is available to get statistics on html
tags/attributes with CSS-like queries.

See the [Queries on
WebDevData](https://github.com/baptistelebail/webdevdata.org/wiki/Queries-on-WebDevData)
wiki.

