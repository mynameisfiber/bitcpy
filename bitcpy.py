#!/usr/local/python

import bitly_api
import xerox
import re
from config import BITLY_API_USERNAME, BITLY_API_PASSWORD, TIMEOUT

bitly = bitly_api.Connection(BITLY_API_USERNAME, BITLY_API_PASSWORD)
if bitly.login is "":
  import sys
  print "Could not log into the bit.ly api services!  Please check your username/password."
  sys.exit(-1)

ltrs    = r'\w'
gunk    = r'/#~:.?+=&%@!\-'
punc    = r'.:?\-'
anychar = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                         'gunk' : gunk,
                                         'punc' : punc }

url = r"""
    \b                             # start at word boundary
    (   (http://|www.)+            # need resource and a colon
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
  if len(matches) > 1:
    url = matches[0]
    if not url.startswith("http://"):
      url = "http://"+url
    if url.startswith("http://bit.ly/"):
      return matches[0]
    try:
      return bitly.shorten(url)["url"]
    except bitly_api.bitly_api.BitlyError:
      print 'Could not shorten url "%s".  This could be a problem with your API key'%url
      return matches[0]
  return ""

def bitify_string(string):
  stringnew, num_sub = find_links.subn(bitify_urlmatch, string)
  print "%s => %s (%d changes)"%(string, stringnew, num_sub)
  return stringnew

if __name__ == "__main__":
  import time

  laststr = ""
  while True:
    newstr = xerox.paste()
    if laststr != newstr and newstr is not "":
      bitified = bitify_string(newstr)
      xerox.copy(bitified)
      laststr = bitified
    time.sleep(TIMEOUT)

