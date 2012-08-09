#!/usr/bin/python
from bs4 import BeautifulSoup
import urlparse
from posixpath import basename, dirname
import urllib2

url = "http://www.mto.gov.on.ca/english/dandv/driver/handbook/index.shtml"
while url:
    page = urllib2.urlopen(url)
    if page:
        try:
            content = unicode(page.read(), "utf-8", errors="replace")
            url = urlparse.urlparse(url)
            filename = basename(url.path)
            # print "filename is: ", filename
            with open(filename, 'w') as f:
                f.write(content.encode("utf-8"))
            soup = BeautifulSoup(content)
            next_page = soup.select("div.next_handbook > a")[0]
        except urllib2.HTTPError, error:
            if error.code == 404:
                print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
            else:
                print >> sys.stderr, "ERROR: %s" % error
        except urllib2.URLError, error:
            print >> sys.stderr, "ERROR: %s" % error

        
        next_filename = next_page["href"] 
        # print "next_filename is: ", next_filename
        assert next_filename == basename(next_filename)
        url = "http://" + url.netloc + dirname(url.path) + "/" + next_filename
        # print "next url is: ", url
