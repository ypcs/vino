#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2012 Ville Korhonen <ville@xd.fi>
# GPLv3
# 
# Lataa lista Goodmoodtv:stä löytyvistä Eduskunta-aiheisista videoista
# tulostaa urlin videon flash-playeriin sekä rtmp-urlin
#
# Itse videon voi ladata esim. rtmpdump -työkalun avulla
# rtmpdump -o output.flv -r rtmpurl

import os
import sys
try:
    from urllib2 import unquote, urlopen
except ImportError:
    try:
        from urllib import unquote, urlopen
    except ImportError:
        print "urllib not found, exiting"
        sys.exit(1)

from xml.dom.minidom import parse, parseString

XML_URL = "http://www.goodmoodtv.com/internettv/application/eduskunta"
POST_BODY = """<request id="105">
	<cmp>fi.goodmood.catalog.Channel</cmp>
	<cmd>listVisibleVideos</cmd>
	<objectid>512698</objectid>
</request>"""

FIELDS = (
    'id',
    'title',
    'subtitle',
    'timestamp',
    'timestamp2',
    'unknown1',
    'category',
    'unknown2',
    'flv_url',
    'rtmp_url',
    'category2',
    'unknown3',
    'unknown4',
    'unknown5',
    'unknown6',
    'unknown7',
    'url',
)



def main():
    if len(sys.argv) == 1:
        dom = parseString(urlopen(XML_URL, data=POST_BODY).read())
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        dom = parse(filename)
    else:
        print "Invalid arguments."
        return 1
    
    data = unquote(dom.getElementsByTagName("data").pop().lastChild.toxml()).split(':')[1].split(',')
    
    for i in range(0, len(data), len(FIELDS)):
        t_fields = data[i:i+len(FIELDS)]
        d = dict(zip(FIELDS, t_fields))
        d['url'] = unquote(d['url'])
        d['flv_url'] = unquote(d['flv_url'])
        d['rtmp_url'] = unquote(d['rtmp_url'])
        
        print d['title'].replace('+', ' ')
        print d['url']
        print d['rtmp_url']
        print    

if __name__ == "__main__":
    sys.exit(main())