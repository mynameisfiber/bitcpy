#!/usr/bin/python

import bitly_api
import xerox
import re
import ConfigParser

try:
  import pynotify
except ImportError:
  pynotify = None

class BitCpy:
  def __init__(self, BITLY_API_USERNAME, BITLY_API_PASSWORD, BITLY_PREFERRED_DOMAIN="bit.ly"):
    self.bitly_urls     = ["http://bitly.com", "http://bit.ly", "http://j.mp"]
    if "http://"+BITLY_PREFERRED_DOMAIN not in self.bitly_urls:
      raise Exception("Invalid preferred domain '%s'!"%BITLY_PREFERRED_DOMAIN)
    self.bitly          = bitly_api.Connection(BITLY_API_USERNAME,
    BITLY_API_PASSWORD,
    preferred_domain    = BITLY_PREFERRED_DOMAIN)
    self.find_links     = self.create_find_links()
    self.minlength      = len("http://" + BITLY_PREFERRED_DOMAIN + "/XXXXXX")

  def create_find_links(self):
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
    
    return re.compile(url, re.VERBOSE | re.MULTILINE) 

  def bitify_urlmatch(self, match):
    matches = match.groups()
    if len(matches) > 1:
      url = matches[0]
      if len(url) <= self.minlength:
        return matches[0]
      if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://"+url
      if any([url.startswith(burl) for burl in self.bitly_urls]):
        return matches[0]
      try:
        return self.bitly.shorten(url)["url"]
      except bitly_api.bitly_api.BitlyError, e:
        self.notify('Could not shorten url "%s".  This could be a problem with your API key.\nerror: bitly_api: %s'%(url,e))
        return matches[0]
    return ""

  def bitify_string(self, string):
    stringnew = self.find_links.sub(self.bitify_urlmatch, string)
    dc = len(string) - len(stringnew)
    if dc > 0:
      self.notify("Shortened clipboard by %d characters!"%dc)
    return stringnew
  
  def notify(self, string):
    if pynotify is not None:
      n = pynotify.Notification("BitCPy", string)
      n.show()
    print string

def main():
  from pkg_resources import Requirement, resource_filename
  import os
  import shutil
  import time

  config = ConfigParser.ConfigParser()
  config.read([resource_filename(Requirement.parse("bitcpy"),"bitcpy/bitcpy.conf"), 
               os.path.expanduser("~/.bitcpyrc")])

  try:
    BITLY_API_USERNAME     = config.get("bitcpy", "BITLY_API_USERNAME")
    BITLY_API_PASSWORD     = config.get("bitcpy", "BITLY_API_PASSWORD")
    TIMEOUT                = config.getfloat("bitcpy", "TIMEOUT")
  except Exception, e:
    import sys
    print e
    sys.exit(-1)
  
  try:
    BITLY_PREFERRED_DOMAIN = config.get("bitcpy", "BITLY_PREFERRED_DOMAIN")
  except ConfigParser.NoOptionError:
    BITLY_PREFERRED_DOMAIN = "bit.ly"

  b = BitCpy(BITLY_API_USERNAME, BITLY_API_PASSWORD, BITLY_PREFERRED_DOMAIN)
  laststr = ""
  while True:
    newstr = xerox.paste()
    if laststr != newstr and newstr is not "":
      bitified = b.bitify_string(newstr)
      xerox.copy(bitified)
      laststr = bitified
    time.sleep(TIMEOUT)

if __name__ == "__main__":
  main()
