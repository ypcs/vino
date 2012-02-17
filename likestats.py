#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2012 Ville Korhonen <ville@xd.fi>
#
# GPLv3
# Skriptin avulla saat ladattua Facebookin likestatsit käyttäen Graph-APIa
#
# Käyttö: likestats.py <tiedosto>, missä <tiedosto> osoittaa tiedostoon, jossa on listattuna FB-sivujen osoitteita tai ID:itä

import os
import sys
import urllib

try:
	import json
except ImportError:
	print "Python >= 2.6 is required for JSON support."
	sys.exit(1)


FB_GRAPH_URL = "https://graph.facebook.com/"
FB_PAGE_URL = "https://www.facebook.com/pages/"
FB_BASEURL_LENGTH = 24

def get_page_id(url):
	if url.startswith(FB_PAGE_URL): # alkaa fb.com/pages, eli sivulla ei ole usernamea
		p = url.index('/', FB_BASEURL_LENGTH + 7) + 1
		return url[p:]
	elif not url.startswith('http'): # ei ole urli vaan sivuid
		return url
	else: # muussa tapauksessa sivulla on username, eli muotoa fb.com/jokusivu
		return url[FB_BASEURL_LENGTH:]

def get_stats(url):
	graph_url = FB_GRAPH_URL + get_page_id(url)
	try:
		data = json.load(urllib.urlopen(graph_url))
	except:
		print >>sys.stderr, "Failure while downloading %s" % url
		data = None
	return data
	

def main():	
	if len(sys.argv) != 2:
		print >>sys.stderr, "Invalid arguments."
		return 1
	
	filename = sys.argv[1]
	if not os.path.exists(filename):
		print >>sys.stderr, "File not found: %s" % filename
		return 1
	
	data = open(filename, "r").readlines()
	
	for url in data:
		data = get_stats(url)
		print '%(id)s,"%(name)s","%(likes)s","%(category)s"' % {
			'id': data['id'],
			'name': data['name'],
			'category': data['category'],
			'likes': data['likes'],
		}
	
	
	
	return 0


if __name__ == "__main__":
	sys.exit(main())