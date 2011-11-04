#!/usr/local/python

import bitly_api
import xerox
import re
from config import BITLY_API_USERNAME, BITLY_API_PASSWORD, TIMEOUT

bitly = bitly_api.Connection(BITLY_API_USERNAME, BITLY_API_PASSWORD)

ltrs    = r'\w'
gunk    = r'/#~:.?+=&%@!\-'
punc    = r'.:?\-'
anychar = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                         'gunk' : gunk,
                                         'punc' : punc }

url = r"""
    \b                             # start at word boundary
    (   (http[s]?://|www.)+        # need resource and a colon
         [%(any)s]  +?             # followed by one or more
                                   #  of any valid character, but
                                   #  be conservative and take only
                                   #  what you need to....
     (?=                           # look-ahead non-consumptive assertion
             [%(punc)s]*           # either 0 or more punctuation
             (?:   [^%(any)s]      #  followed by a non-url char
                 |                 #   or end of the string
                   $
             )
     )
    )
    """ % {'any' : anychar,
           'punc' : punc }

find_links = re.compile(url, re.VERBOSE | re.MULTILINE) 

def bitify_urlmatch(match):
  matches = match.groups()
  print matches
  if len(matches) > 1:
    url = matches[0]
    if not url.startswith("http://"):
      url = "http://"+url
    return bitly.shorten(url)["url"]
  return ""

def bitify_string(string):
  string, num_sub = find_links.subn(bitify_urlmatch, string)
  print "New string: ",string
  return string

if __name__ == "__main__":
  import time

  laststr = None
  while True:
    newstr = xerox.paste()
    if laststr != newstr and newstr is not "":
      print "New: %s, Old: %s"%(laststr, newstr)
      bitified = bitify_string(newstr)
      print "Copying ",bitified
      xerox.copy(bitified)
      laststr = bitified
    time.sleep(TIMEOUT)

